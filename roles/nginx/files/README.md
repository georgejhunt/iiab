### Transition to NGINX
1. Initial testing strategy is to insert nginx undder apache, and proxy everything to apache -- creating a shim.
2. Without php available via fastcgi, any function at all for php based applications validates nginx.
3. Current state (7/15/19):
    1. Principal functions migrated to nginx.
         * Admin Console
         * Awstats
         * kiwix -- goes directly to port 3000
         * kalite -- goes directly to port 8009
         * calibre-web
         * kolibri
    2. Still proxied to Apache
         * mediawiki
         * elgg
         * nodered
         * nextcloud
         * wordpress
         * moodle
         * archive.org
