#!/usr/bin/python3

"""
This script is designed to integrate with a static site generator (like LSTE) 
to automate the creation and saving of an RSS feed. The RSS feed is generated 
based on the site's content and configuration settings and is saved as an XML 
file in the site's distribution directory.

Key Features:
- Automatically registers hooks to trigger RSS feed generation after site content is rendered.
- Constructs a valid RSS 2.0 feed including metadata and articles.
- Saves the generated RSS feed to a file named 'feed.xml' in the specified output directory.

Legal Note:
 - Written and maintained by Laura Herzog (laura-herzog@outlook.com)
 - Licensed under the GPL license. See the project at https://github.com/lauratheq/lste
"""

import re
from datetime import datetime
from typing import Any

def register_hooks(lste: Any) -> None:
    """
    Registers the necessary hooks for generating and saving an RSS feed.

    This function adds hooks to the `lste` object to ensure that the RSS feed
    is generated after the content is rendered and saved after the site is saved.

    Args:
        lste (Any): The site object, which is expected to have a `hooks` attribute
                    where functions can be added to specific events.
    """
    lste.hooks.add('after_render_content', generate_rss)
    lste.hooks.add('after_save_site', save_rss_file)

def generate_rss(lste: Any) -> Any:
    """
    Generates an RSS feed based on the site's content and configuration.

    This function constructs an RSS feed in XML format using the site's content and
    configuration settings. The feed includes details such as the site's title, description,
    language, and each article's title, link, publication date, and description.

    Args:
        lste (Any): The site object, which contains configuration settings, content data,
                    and plugin variables where the generated RSS feed will be stored.

    Returns:
        Any: The modified site object (`lste`) with the generated RSS feed stored in
             `lste.plugin_vars['rss']`.
    """

    # Set the base parameters
    version = lste.version
    title = lste.config_file['lste']['title']
    description = lste.config_file['lste']['description']
    home_url = lste.config_file['rss']['home_url']
    language = lste.config_file['rss']['language']
    contact = lste.config_file['rss']['contact']
    author = lste.config_file['rss']['author']
    image = lste.config_file['rss']['image']

    # Get the current date and time in UTC
    now = datetime.utcnow()
    formatted_date = now.strftime('%a, %d %b %Y %H:%M:%S +0000')

    # Begin constructing the RSS feed
    feed_content = '<rss xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:wfw="http://wellformedweb.org/CommentAPI/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:sy="http://purl.org/rss/1.0/modules/syndication/" xmlns:slash="http://purl.org/rss/1.0/modules/slash/" version="2.0">';
    feed_content += f"""
        <channel>
            <title>{title}</title>
            <atom:link href="{home_url}/rss.xml" rel="self" type="application/rss+xml"/>
            <link>{home_url}</link>
            <description>{description}</description>
            <lastBuildDate>{formatted_date}</lastBuildDate>
            <language>{language}</language>
            <generator>LSTE {version}</generator>
            <sy:updatePeriod>hourly</sy:updatePeriod>
            <sy:updateFrequency>1</sy:updateFrequency>
            <managingEditor>{contact} ({author})</managingEditor>
            <webMaster>{contact} ({author})</webMaster>
            <image>
                <url>{image}</url>
                <title>{title}</title>
                <link>{home_url}</link>
                <width>32</width>
                <height>32</height>
            </image>"""

    # Loop through each article and add it to the RSS feed
    for article in lste.plugin_vars['articles']['articles']:
        content = lste.content[article]
        excerpt_stripped = re.sub(r'<.*?>', '', content['excerpt'])

        date_obj = datetime.strptime(content['meta']['date'], "%d.%m.%Y")
        formatted_date = date_obj.strftime("%a, %d %b %Y %H:%M:%S +0000")

        feed_content += f"""
            <item>
                <title>{content['title']}</title>
                <link>{home_url}/{content['meta']['permalink']}</link>
                <pubDate>{formatted_date}</pubDate>
                <author>{contact} ({author})</author>
                <guid isPermaLink="true">{home_url}/{content['meta']['permalink']}</guid>
                <description>{excerpt_stripped}</description>
                <content:encoded>
                    <![CDATA[ {excerpt_stripped} ]]>
                </content:encoded>
            </item>"""

    # Finalize the RSS feed
    feed_content += '</channel></rss>'
    lste.plugin_vars['rss'] = feed_content

    return lste

def save_rss_file(lste: Any) -> Any:
    """
    Saves the generated RSS feed to a file.

    This function writes the RSS feed content stored in `lste.plugin_vars['rss']`
    to a file named 'feed.xml' in the site's distribution path.

    Args:
        lste (Any): The site object containing the generated RSS feed and distribution path.

    Returns:
        Any: The modified site object (`lste`) after saving the RSS feed to a file.
    """

    # Get feed content
    feed_content = lste.plugin_vars['rss']

    # Write the file
    with open(f'{lste.dist_path}/feed.xml', "w") as handle:
        handle.write(feed_content)

    return lste
