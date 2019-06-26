////
// Persistent, user-specific marker for the most recent time the emails were checked.
////

var STAMP = "STAMP";

function restamp(){
  var properties = PropertiesService.getUserProperties();
  var stamp = properties.getProperty(STAMP);
  if(null == stamp){
    stamp = new Date().getTime();
  }
  properties.setProperty(STAMP, new Date().getTime());
  return(stamp);
}

////
// Obtain recent emails
////

function fresh(){
  var recent = [];
  var stamp = restamp();
  var threads = GmailApp.getTrashThreads();
  for(var i = 0; i < threads.length; i++){
    var thread = threads[i];
    if(thread.getLastMessageDate().getTime() < stamp){
      continue;
    }
    var messages = thread.getMessages();
    for(var j = 0; j < messages.length; j++){
      var message = messages[j];
      if(message.getDate().getTime() >= stamp){
        var attachments = message.getAttachments();
        for(var k = 0; k < attachments.length; k++){
          var attachment = attachments[k];
          recent.push(attachment);
        }
      }
    }
  }
  return(recent);
}

////
// Upload attachments to Google Drive
////

function upload(attachments){
  for(var i = 0; i < attachments.length; i++){
    var attachment = attachments[i];
    Logger.log(attachment.getName());
    DriveApp.createFile(attachment)
  }
}

////
// Main function
////

function main(){
  Logger.log(new Date());
  var attachments = fresh();
  upload(attachments);
}
