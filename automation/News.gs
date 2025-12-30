const RECIPIENT = PropertiesService.getScriptProperties().getProperty('RECIPIENT');
const VERBATIM_FEEDS = JSON.parse(PropertiesService.getScriptProperties().getProperty('VERBATIM_FEEDS'));
const PROMPTED_FEEDS = JSON.parse(PropertiesService.getScriptProperties().getProperty('PROMPTED_FEEDS'));
const RETRIES = 5;
const SLEEP = 10000;
const FORWARDED = 'FORWARDED';
const DEFAULT_FORWARDED = '{}';
const WEEK = 7 * 24 * 60 * 60 * 1000;
const GEMINI_API_KEY = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
const GEMINI_API = `https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent`;

function children(element, name) {
  const result = [];
  element.getChildren().forEach(child => {
    if (child.getName() == name) {
      result.push(child);
    }
  });
  return result;
}

function items(root) {
  Logger.log('Trying: RSS (root)');
  const rootItems = children(root, 'item');
  if (rootItems.length != 0) {
    return rootItems;
  }
  Logger.log('Trying: RSS (channel)');
  const channel = children(root, 'channel');
  if (channel != null && channel.length > 0) {
    const channelItems = children(children(root, 'channel')[0], 'item');
    if (channelItems.length != 0) {
      return channelItems;
    }
  }
  Logger.log('Trying: Atom');
  const atomItems = children(root, 'entry');
  if (atomItems.length != 0) {
    return atomItems;
  }
  return [];
}

function title(item) {
  return children(item, 'title')[0].getText().trim();
}

function link(item) {
  const container = children(item, 'link')[0];
  var url = '';
  // RSS
  container.getAttributes().forEach(attribute => {
    if (attribute.getName() == 'href') {
      url = attribute.getValue();
    }
  })
  // Atom
  if (url == '') {
    try {
      url = container.getText();
    } catch (ignored) {
    }
  }
  return url.trim();
}

function description(item) {
  const description = children(item, 'description');
  if (description != null && description.length > 0) {
    return description[0].getText().trim();
  } else {
    return '';
  }
}

function verbatim() {
  const properties = PropertiesService.getUserProperties();
  if (properties.getProperty(FORWARDED) == null) {
    properties.setProperty(FORWARDED, DEFAULT_FORWARDED);
  }
  const now = new Date().getTime();
  const expiry = now + 4 * WEEK;
  var forwarded = JSON.parse(properties.getProperty(FORWARDED));
  const active = new Set();
  Object.keys(VERBATIM_FEEDS).forEach(feed => {
    try {
      Logger.log('Feed: ' + feed);
      const response = UrlFetchApp.fetch(VERBATIM_FEEDS[feed]);
      const xml = response.getContentText();
      const document = XmlService.parse(xml);
      const root = document.getRootElement();
      items(root).reverse().forEach(item => {
        const subject = title(item);
        const url = link(item);
        const content = description(item);
        active.add(url);
        if (!(url in forwarded)) {
          Logger.log('---');
          Logger.log(subject);
          Logger.log(url);
          Logger.log(content);
          MailApp.sendEmail(
            RECIPIENT,
            `${feed}: ${subject}`,
            '',
            {
              htmlBody: `<html><a href="${url}">${subject}</a><br/>${content}</html>`
            }
          );
          forwarded[url] = expiry;
        }
      });
    } catch (error) {
      Logger.log('Error processing news feed: ' + error.toString());
      throw error;
    }
  });
  for (const url in forwarded) {
    if (forwarded[url] < now) {
      delete forwarded[url];
    }
  }
  properties.setProperty(FORWARDED, JSON.stringify(forwarded));
}

function gemini(prompt) {
  const payload = {
    'contents': [
      {
        'parts': [
          {
            'text': prompt + ` Stick to time span ${span()}.`
          },
        ],
      },
    ],
  };
  const options = {
    method: 'POST',
    contentType: 'application/json',
    headers: {
      'x-goog-api-key': GEMINI_API_KEY,
    },
    payload: JSON.stringify(payload)
  };
  var response = null;
  for (let attempt = 0; attempt < RETRIES; attempt++) {
    try {
      response = UrlFetchApp.fetch(GEMINI_API, options);
      break;
    } catch (exception) {
      Logger.log('Error: ' + exception.message);
      Utilities.sleep(SLEEP);
    }
  }
  if (response == null) {
    return null;
  }
  const data = JSON.parse(response);
  return data['candidates'][0]['content']['parts'][0]['text'];
}

function prompted() {
  Object.keys(PROMPTED_FEEDS).forEach(feed => {
    try {
      Logger.log('Feed: ' + feed);
      const reply = gemini(PROMPTED_FEEDS[feed])
      const subject = feed;
      const content = reply;
      Logger.log('---');
      Logger.log(subject);
      Logger.log(content);
      if (content != null) {
        MailApp.sendEmail(
          RECIPIENT,
          feed,
          '',
          {
            htmlBody: `<html>${subject}<br/>${content}</html>`
          }
        );
      }
    } catch (error) {
      Logger.log('Error processing news feed: ' + error.toString());
      throw error;
    }
  });
}

function reset() {
  PropertiesService.getUserProperties().setProperty(FORWARDED, DEFAULT_FORWARDED);
}

function span() {
  const now = new Date().toLocaleDateString('en-UK', {'year': 'numeric', 'month': 'long', 'day': 'numeric'});
  const then = new Date(new Date().getTime() - WEEK).toLocaleDateString('en-UK', {'year': 'numeric', 'month': 'long', 'day': 'numeric'});
  return `from ${then} to ${now}`;
}
