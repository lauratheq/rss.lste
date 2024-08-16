# LSTE Plugin: RSS Feed Generator

This plugin for [Lauras Simple Template Engine (LSTE)](https://github.com/lauratheq/lste) automates the creation and saving of an RSS feed for your static site. The RSS feed is generated based on your site's content and configuration settings and is saved as an XML file, ready for distribution.

## Installation

1. Add the plugin to your LSTE configuration by including it in your `.listerc` file:

    ```ini
    [plugins]
    rss-feed-generator = lauratheq/rss-feed-generator.lste
    ```

2. LSTE will automatically download and activate the plugin during the next site generation.

## Configuration

You need to define some RSS-specific settings in your `lste.conf` file under the `[rss]` section:

```ini
[rss]
home_url = https://yoursite.com
language = en-EN
contact = contact@yoursite.com
author = Your Name
image = https://yoursite.com/logo.png
```

## Contributing

### Contributor Code of Conduct

Please note that this project is adapting the [Contributor Code of Conduct](https://learn.wordpress.org/online-workshops/code-of-conduct/) from WordPress.org even though this is not a WordPress project. By participating in this project, you agree to abide by its terms.

### Basic Workflow

* Grab an issue
* Fork the project
* Add a branch with the number of your issue
* Develop your changes
* Commit to your forked project
* Send a pull request to the main branch with all the details

Please make sure that you have [set up your user name and email address](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup) for use with Git. Strings such as `silly nick name <root@localhost>` look unprofessional in the commit history of a project.

Due to time constraints, you may not always get a quick response. Please do not take delays personally and feel free to send a reminder.

### Workflow Process

* Every new issue gets the label 'Request'
* Every commit must be linked to the issue with the following pattern: `#${ISSUENUMBER} - ${MESSAGE}`
* Every PR should contain one commit and reference a specific issue
