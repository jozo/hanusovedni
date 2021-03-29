module Main exposing (..)

import Browser
import Html exposing (Attribute, Html, a, address, article, div, footer, h3, img, input, label, li, option, select, span, text, time, ul)
import Html.Attributes exposing (alt, attribute, class, datetime, for, height, href, id, src, style, title, type_, value, width)
import Html.Attributes.Extra exposing (role)
import Html.Events exposing (onCheck, onInput)
import Html.Events.Extra exposing (onChange)
import Http
import Json.Decode as D
import Set
import String.Normalize exposing (removeDiacritics)



-- In memory of Rakyi who introduced me to Elm
-- MAIN


main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }



-- MODEL


type alias Event =
    { title : String
    , url : String
    , dateAndTime : EventDateAndTime
    , location : String
    , speakers : Speakers
    , extendedInfo : EventExtendedInfo
    }


type alias EventDateAndTime =
    { iso : String
    , repr : String
    }


type alias Speakers =
    { underLimit : List String
    , overLimitNames : String
    , overLimitCount : Int
    }


type alias EventExtendedInfo =
    { hasVideo : Bool
    , category : EventCategory
    , festival : String
    , icon : Maybe EventIcon
    }


type alias EventCategory =
    { title : String
    , color : String
    }


type alias EventIcon =
    { title : String
    , url : String
    }


type ModelState
    = Failure Http.Error
    | Loading
    | Success (List Event)


type Language
    = SK
    | EN


type alias Model =
    { state : ModelState
    , language : Language
    , category : String
    , year : String
    , withVideo : Bool
    , searchText : String
    , festival : String
    }


init : String -> ( Model, Cmd Msg )
init languageCode =
    ( Model Loading (decodeLanguage languageCode) "---" "---" False "" "---", getAllEvents languageCode )


decodeLanguage : String -> Language
decodeLanguage languageCode =
    case String.toUpper languageCode of
        "SK" ->
            SK

        "EN" ->
            EN

        _ ->
            EN



-- UPDATE


type Msg
    = GotEvents (Result Http.Error (List Event))
    | SetCategoryFilter String
    | SetYearFilter String
    | SetVideoFilter Bool
    | SetSearchText String
    | SetFestivalFilter String


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        GotEvents result ->
            case result of
                Ok events ->
                    ( { model | state = Success events }, Cmd.none )

                Err error ->
                    ( { model | state = Failure error }, Cmd.none )

        SetCategoryFilter category ->
            ( { model | category = category }, Cmd.none )

        SetYearFilter year ->
            ( { model | year = year }, Cmd.none )

        SetVideoFilter value ->
            ( { model | withVideo = value }, Cmd.none )

        SetSearchText text ->
            ( { model | searchText = text }, Cmd.none )

        SetFestivalFilter text ->
            ( { model | festival = text }, Cmd.none )



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions _ =
    Sub.none



-- VIEW


view : Model -> Html Msg
view model =
    case model.state of
        Failure error ->
            div []
                [ text "I could not load events for some reason. "
                , case error of
                    Http.BadUrl msg ->
                        text msg

                    Http.BadBody msg ->
                        text msg

                    _ ->
                        text ""
                ]

        Loading ->
            text "Loading..."

        Success events ->
            div [ class "row" ]
                [ viewFilters model.language events
                , viewEvents model events
                ]


viewFilters : Language -> List Event -> Html Msg
viewFilters lang events =
    let
        categories =
            events
                |> List.map (\e -> e.extendedInfo.category.title)
                |> Set.fromList
                |> Set.toList

        categoryLabel =
            case lang of
                SK ->
                    "Kategória:"

                EN ->
                    "Category:"

        years =
            events
                |> List.map (\e -> String.slice 0 4 e.dateAndTime.iso)
                |> Set.fromList
                |> Set.toList
                |> List.sort
                |> List.reverse

        yearLabel =
            case lang of
                SK ->
                    "Rok:"

                EN ->
                    "Year:"

        withVideoLabel =
            case lang of
                SK ->
                    "Len s videom"

                EN ->
                    "Only with video"

        searchLabel =
            case lang of
                SK ->
                    "Hľadať"

                EN ->
                    "Search"

        festivals =
            events
                |> List.map (\e -> e.extendedInfo.festival)
                |> Set.fromList
                |> Set.toList
                |> List.sort

        festivalLabel =
            case lang of
                SK ->
                    "Festival"

                EN ->
                    "Festival"
    in
    div [ class "col-12" ]
        [ div
            [ id "filter-panel"
            , class "mb-1 d-flex flex-wrap align-items-center"
            ]
            [ div [ class "m-2" ]
                [ label [ for "searchInput", class "mb-0 mx-2" ] [ text searchLabel ]
                , input
                    [ type_ "text"
                    , id "searchInput"
                    , class "mx-2"
                    , onInput SetSearchText
                    ]
                    []
                ]
            , div [ class "m-2" ]
                [ label [ for "festivalSelect", class "mb-0 mx-2" ] [ text festivalLabel ]
                , select [ id "festivalSelect", onChange SetFestivalFilter ]
                    ([ option [ value "---" ] [ text "---" ] ]
                        ++ List.map (\f -> option [ value f ] [ text f ]) festivals
                    )
                ]
            , div [ class "m-2" ]
                [ label [ for "categorySelect", class "mb-0 mx-2" ] [ text categoryLabel ]
                , select [ id "categorySelect", onChange SetCategoryFilter ]
                    ([ option [ value "---" ] [ text "---" ] ]
                        ++ List.map (\c -> option [ value c ] [ text c ]) categories
                    )
                ]
            , div [ class "m-2" ]
                [ label [ for "yearSelect", class "mb-0 mx-2" ] [ text yearLabel ]
                , select [ id "yearSelect", onChange SetYearFilter ]
                    ([ option [ value "---" ] [ text "---" ] ]
                        ++ List.map (\y -> option [ value y ] [ text y ]) years
                    )
                ]
            , div [ class "m-2" ]
                [ input
                    [ type_ "checkbox"
                    , id "withVideoInput"
                    , class "mx-2"
                    , onCheck SetVideoFilter
                    ]
                    []
                , label [ for "withVideoInput", class "mb-0" ] [ text withVideoLabel ]
                ]
            ]
        ]


viewEvents : Model -> List Event -> Html Msg
viewEvents model events =
    let
        filteredEvents =
            filterEvents model events
    in
    div [ class "col-12" ]
        [ div
            [ class "row mx-n02 justify-content-center w-100" ]
            (if List.isEmpty filteredEvents then
                [ viewMessageEmpty model.language ]

             else
                List.map (viewEvent model.language) filteredEvents
            )
        ]


viewMessageEmpty : Language -> Html Msg
viewMessageEmpty lang =
    div [ class "col-8 mx-auto text-center" ]
        [ div [ class "alert alert-warning mt-3", role "alert" ]
            [ case lang of
                SK ->
                    text "Nenašli sa podujatia pre zadané kritériá 😥"

                EN ->
                    text "No events found for specified criteria 😥"
            ]
        ]


filterEvents : Model -> List Event -> List Event
filterEvents model events =
    filterByText model.searchText
        (filterByVideo model.withVideo
            (filterByYear model.year
                (filterByCategory model.category (filterByFestival model.festival events))
            )
        )


filterByFestival : String -> List Event -> List Event
filterByFestival festival events =
    if festival == "---" then
        events

    else
        List.filter (\e -> e.extendedInfo.festival == festival) events


filterByText : String -> List Event -> List Event
filterByText text events =
    if String.isEmpty text then
        events

    else
        List.filter (\e -> containsText text e.title) events


containsText : String -> String -> Bool
containsText left right =
    String.contains (removeDiacritics (String.toLower left)) (removeDiacritics (String.toLower right))


filterByCategory : String -> List Event -> List Event
filterByCategory category events =
    if category == "---" then
        events

    else
        List.filter (\e -> e.extendedInfo.category.title == category) events


filterByYear : String -> List Event -> List Event
filterByYear year events =
    if year == "---" then
        events

    else
        List.filter (\e -> String.slice 0 4 e.dateAndTime.iso == year) events


filterByVideo : Bool -> List Event -> List Event
filterByVideo withVideo events =
    if not withVideo then
        events

    else
        List.filter (\e -> e.extendedInfo.hasVideo) events


viewEvent : Language -> Event -> Html Msg
viewEvent lang event =
    div [ class "col-lg-3 col-md-4 col-sm-6 col-12 d-flex px-02 mb-1 overflow-hidden" ]
        [ a [ href event.url, class "d-flex w-100 text-decoration-none" ]
            [ article
                [ class "event d-flex flex-column"
                , style "background-color" event.extendedInfo.category.color
                ]
                [ div
                    [ class "illustration d-flex justify-content-center align-items-center" ]
                    [ viewEventIcon event.extendedInfo.icon ]
                , div [ class "category" ]
                    [ div [ class "name" ] [ text event.extendedInfo.category.title ] ]
                , div [ class "content" ]
                    [ h3 [] [ text event.title ]
                    , viewSpeakers lang event.speakers
                    ]
                , footer []
                    [ time
                        [ class "d-flex align-items-center"
                        , datetime event.dateAndTime.iso
                        ]
                        [ text event.dateAndTime.repr ]
                    , address [ class "py-2 d-flex align-items-center" ] [ text event.location ]
                    ]
                ]
            ]
        ]


viewEventIcon : Maybe EventIcon -> Html Msg
viewEventIcon maybeIcon =
    case maybeIcon of
        Nothing ->
            text ""

        Just icon ->
            img [ alt icon.title, src icon.url, width 65, height 65, attribute "loading" "lazy" ] []


viewSpeakers : Language -> Speakers -> Html Msg
viewSpeakers lang speakers =
    if speakers.overLimitCount <= 0 then
        ul [ class "speakers" ] (List.map viewSpeaker speakers.underLimit)

    else
        let
            normalSpeakers =
                List.take ((List.length speakers.underLimit) - 1) speakers.underLimit

            lastSpeaker =
                viewLastSpeaker
                    lang
                    (List.head (List.reverse speakers.underLimit))
                    speakers.overLimitCount
                    speakers.overLimitNames
        in
        ul [ class "speakers" ] (List.map viewSpeaker normalSpeakers ++ [ lastSpeaker ])


viewSpeaker : String -> Html Msg
viewSpeaker speaker =
    li [] [ text speaker ]


viewLastSpeaker : Language -> Maybe String -> Int -> String -> Html Msg
viewLastSpeaker lang maybeSpeaker overLimit overLimitNames =
    case maybeSpeaker of
        Nothing ->
            text ""

        Just speaker ->
            li []
                [ text speaker
                , span [ title overLimitNames ]
                    [ text
                        (" + "
                            ++ String.fromInt overLimit
                            ++ (case lang of
                                    SK ->
                                        " ďalší"

                                    EN ->
                                        " more"
                               )
                        )
                    ]
                ]



-- HTTP


getAllEvents : String -> Cmd Msg
getAllEvents languageCode =
    Http.get
        { url = "/" ++ languageCode ++ "/events/json/"
        , expect = Http.expectJson GotEvents eventsDecoder
        }


eventsDecoder : D.Decoder (List Event)
eventsDecoder =
    D.field "events" (D.list eventDecoder)


eventDecoder : D.Decoder Event
eventDecoder =
    D.map6 Event
        (D.field "title" D.string)
        (D.field "url" D.string)
        (D.field "dateAndTime" eventDateAndTimeDecoder)
        (D.field "location" D.string)
        (D.field "speakers" speakersDecoder)
        (D.field "extendedInfo" eventExtendedInfoDecoder)


eventDateAndTimeDecoder : D.Decoder EventDateAndTime
eventDateAndTimeDecoder =
    D.map2 EventDateAndTime
        (D.field "iso" D.string)
        (D.field "repr" D.string)


eventExtendedInfoDecoder : D.Decoder EventExtendedInfo
eventExtendedInfoDecoder =
    D.map4 EventExtendedInfo
        (D.field "hasVideo" D.bool)
        (D.field "category" eventCategoryDecoder)
        (D.field "festival" D.string)
        (D.field "icon" (D.nullable eventIconDecoder))


eventCategoryDecoder : D.Decoder EventCategory
eventCategoryDecoder =
    D.map2 EventCategory
        (D.field "title" D.string)
        (D.field "color" D.string)


eventIconDecoder : D.Decoder EventIcon
eventIconDecoder =
    D.map2 EventIcon
        (D.field "title" D.string)
        (D.field "url" D.string)


speakersDecoder : D.Decoder Speakers
speakersDecoder =
    D.map3 Speakers
        (D.field "under_limit" (D.list D.string))
        (D.field "over_limit_names" D.string)
        (D.field "over_limit_count" D.int)
