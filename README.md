HanusoveDni.sk
==============

# TODO add how to start develop

docker network create hanus-net

s = Site.objects.get()
s.hostname = "hanusovedni.online"
s.port = 443
s.save()

from django.core.cache import cache
cache.clear()

Monitoring
----------
https://uptimerobot.com/


### Logz.io
```shell script
docker run --name docker-collector-metrics \
-d --restart=always \
--env LOGZIO_TOKEN="{{METRICS TOKEN}}" \
--env LOGZIO_MODULES="docker" \
--env LOGZIO_REGION="eu" \
-v /var/run/docker.sock:/var/run/docker.sock:ro \
logzio/docker-collector-metrics


docker run --name docker-collector-logs \
-d --restart=always \
--env LOGZIO_TOKEN="{{ACCOUNT TOKEN}}" \
--env LOGZIO_URL="listener-eu.logz.io:5015" \
-v /var/run/docker.sock:/var/run/docker.sock:ro \
-v /var/lib/docker/containers:/var/lib/docker/containers \
logzio/docker-collector-logs
```

DB backup
---------
```shell script
pg_dump -U hanusovedni -d hanusovedni > /code/backup.sql
psql -U hanusovedni -d hanusovedni < /code/backup.sql

pg_dump -U hanusovedni -d hanusovedni | gzip > /code/backup.sql.gz
gunzip -c /code/backup.sql.gz | psql -U hanusovedni -d hanusovedni
```

DB console
----------
```shell script
psql -U hanusovedni -d hanusovedni
```

Import data from blank state
-----------------------------------
```shell script
./manage.py migrate
./manage.py createsuperuser
# create BHD, KHD, SpeakerIndex and EventIndex manually through Wagtail admin
./manage.py import_data -c /media_root/ -i /media_root/imp_images/
```


SQL to import data from WordPress
---------------------------------

### Categories
```sql
select distinct meta_value as category from wp_postmeta
where meta_key = '_bhd_event_topic'
```

### Locations
```sql
select distinct TRIM(Replace(Replace(Replace(meta_value,'\t',''),'\n',''),'\r','')) as location from wp_postmeta
where meta_key = '_bhd_event_location'
order by location
```

### Speakers
```sql
SELECT speakers.ID,
       speakers.post_date,
       speakers.post_title,
       speakers.post_name,
       files.meta_value AS filename,
       speakers.guid,
       speakers.post_content
from wp_posts as speakers
         left join wp_postmeta meta on (speakers.ID = meta.post_id and meta.meta_key = '_thumbnail_id')
         left join wp_postmeta files on (files.post_id = meta.meta_value and files.meta_key = '_wp_attached_file')
where speakers.post_type = 'bhd_speaker'
  and speakers.post_status = 'publish'
order by speakers.ID
```

### Events
```sql
SELECT events.ID,
       events.post_date,
       events.post_title,
       events.post_name,
       events.post_content,
       meta1.meta_value           as short_title,
       meta2.meta_value           as short_speaker_names,
       meta3.meta_value           as speaker_names,
       meta4.meta_value           as questions,
       meta5.meta_value           as location,
       meta6.meta_value           as datetime,
       meta7.meta_value           as topic,
       meta8.meta_value           as youtube_link,
       meta9.meta_value           as illustration,
       meta10.meta_value          as tickets_free_entry,
       meta11.meta_value          as google_maps_link,
       meta12.meta_value          as overview,
       meta13.meta_value          as show_in_program,
       meta14.meta_value          as tickets_button_url,
       meta15.meta_value          as tickets_button_label,
       meta16.meta_value          as after_event_text,
       (select group_concat(wp_p2p.p2p_to SEPARATOR ',')
        from wp_p2p
        where wp_p2p.p2p_from = events.ID
        group by wp_p2p.p2p_from) as speakers
from wp_posts as events
         left join wp_postmeta meta1 on (events.ID = meta1.post_id and meta1.meta_key = '_bhd_event_short_title')
         left join wp_postmeta meta2
                   on (events.ID = meta2.post_id and meta2.meta_key = '_bhd_event_short_speaker_names')
         left join wp_postmeta meta3 on (events.ID = meta3.post_id and meta3.meta_key = '_bhd_event_speaker_names')
         left join wp_postmeta meta4 on (events.ID = meta4.post_id and meta4.meta_key = '_bhd_event_questions')
         left join wp_postmeta meta5 on (events.ID = meta5.post_id and meta5.meta_key = '_bhd_event_location')
         left join wp_postmeta meta6 on (events.ID = meta6.post_id and meta6.meta_key = '_bhd_event_datetime')
         left join wp_postmeta meta7 on (events.ID = meta7.post_id and meta7.meta_key = '_bhd_event_topic')
         left join wp_postmeta meta8 on (events.ID = meta8.post_id and meta8.meta_key = '_bhd_event_youtube_link')
         left join wp_postmeta meta9 on (events.ID = meta9.post_id and meta9.meta_key = '_bhd_event_illustration')
         left join wp_postmeta meta10 on (events.ID = meta10.post_id and meta10.meta_key = '_bhd_tickets_free_entry')
         left join wp_postmeta meta11
                   on (events.ID = meta11.post_id and meta11.meta_key = '_bhd_event_google_maps_link')
         left join wp_postmeta meta12 on (events.ID = meta12.post_id and meta12.meta_key = '_bhd_event_overview')
         left join wp_postmeta meta13 on (events.ID = meta13.post_id and meta13.meta_key = '_bhd_event_show_in_program')
         left join wp_postmeta meta14 on (events.ID = meta14.post_id and meta14.meta_key = '_bhd_tickets_button_url')
         left join wp_postmeta meta15 on (events.ID = meta15.post_id and meta15.meta_key = '_bhd_tickets_button_label')
         left join wp_postmeta meta16 on (events.ID = meta16.post_id and meta16.meta_key = '_bhd_event_after_event')
where events.post_type = 'event'
  and events.post_status = 'publish'
order by events.ID
```
