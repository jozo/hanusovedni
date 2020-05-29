module Main exposing (..)

import Browser
import Html exposing (Attribute, Html, a, address, article, div, footer, h3, img, input, label, li, option, select, span, text, time, ul)
import Html.Attributes exposing (alt, class, datetime, for, height, href, id, src, style, title, type_, value, width)
import Html.Attributes.Extra exposing (role)
import Html.Events exposing (onCheck)
import Html.Events.Extra exposing (onChange)
import Http
import Json.Decode as D
import Set



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
    , hasVideo : Bool
    , location : String
    , category : EventCategory
    , icon : Maybe EventIcon
    , speakers : Speakers
    }


type alias EventDateAndTime =
    { iso : String
    , repr : String
    }


type alias EventCategory =
    { title : String
    , color : String
    }


type alias EventIcon =
    { title : String
    , url : String
    }


type alias Speakers =
    { underLimit : List String
    , overLimitNames : String
    , overLimitCount : Int
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
    }


init : String -> ( Model, Cmd Msg )
init languageCode =
    ( Model Loading (decodeLanguage languageCode) "---" "---" False, getAllEvents languageCode )


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
                |> List.map (\e -> e.category.title)
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
    in
    div [ class "col-12" ]
        [ div
            [ id "filter-panel"
            , class "p-2 mb-1 d-flex justify-content-center align-items-center"
            ]
            [ label [ for "categorySelect", class "mb-0 mx-2" ] [ text categoryLabel ]
            , select [ id "categorySelect", onChange SetCategoryFilter ]
                ([ option [ value "---" ] [ text "---" ] ]
                    ++ List.map (\c -> option [ value c ] [ text c ]) categories
                )
            , label [ for "yearSelect", class "mb-0 mx-2" ] [ text yearLabel ]
            , select [ id "yearSelect", onChange SetYearFilter ]
                ([ option [ value "---" ] [ text "---" ] ]
                    ++ List.map (\y -> option [ value y ] [ text y ]) years
                )
            , input
                [ type_ "checkbox"
                , id "withVideoInput"
                , class "mx-2"
                , onCheck SetVideoFilter
                ]
                []
            , label [ for "withVideoInput", class "mb-0" ] [ text withVideoLabel ]
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
    filterByVideo model.withVideo
        (filterByYear model.year
            (filterByCategory model.category events)
        )


filterByCategory : String -> List Event -> List Event
filterByCategory category events =
    if category == "---" then
        events

    else
        List.filter (\e -> e.category.title == category) events


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
        List.filter .hasVideo events


viewEvent : Language -> Event -> Html Msg
viewEvent lang event =
    div [ class "col-lg-3 col-md-4 col-sm-6 col-12 d-flex px-02 mb-1 overflow-hidden" ]
        [ a [ href event.url, class "d-flex w-100 text-decoration-none" ]
            [ article
                [ class "event d-flex flex-column"
                , style "background-color" event.category.color
                ]
                [ div
                    [ class "illustration d-flex justify-content-center align-items-center" ]
                    [ viewEventIcon event.icon ]
                , div [ class "category" ]
                    [ div [ class "name" ] [ text event.category.title ] ]
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
            img [ alt icon.title, src icon.url, width 65, height 65 ] []


viewSpeakers : Language -> Speakers -> Html Msg
viewSpeakers lang speakers =
    if speakers.overLimitCount <= 0 then
        ul [ class "speakers" ] (List.map viewSpeaker speakers.underLimit)

    else
        let
            normalSpeakers =
                List.take (List.length speakers.underLimit) speakers.underLimit

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
    D.map8 Event
        (D.field "title" D.string)
        (D.field "url" D.string)
        (D.field "dateAndTime" eventDateAndTimeDecoder)
        (D.field "hasVideo" D.bool)
        (D.field "location" D.string)
        (D.field "category" eventCategoryDecoder)
        (D.field "icon" (D.nullable eventIconDecoder))
        (D.field "speakers" speakersDecoder)


eventDateAndTimeDecoder : D.Decoder EventDateAndTime
eventDateAndTimeDecoder =
    D.map2 EventDateAndTime
        (D.field "iso" D.string)
        (D.field "repr" D.string)


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
