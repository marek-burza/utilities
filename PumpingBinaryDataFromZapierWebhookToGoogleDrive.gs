function establishFolder(root, name){
  var folders = root.getFoldersByName(name);
  if(folders.hasNext()){
    return folders.next();
  }else{
    return root.createFolder(name);
  }
} 

function pumpRoot(){
  return establishFolder(DriveApp.getRootFolder(), "Pump");
}

function pumpInbox(){
  return establishFolder(pumpRoot(), "PumpIn");
}

function pumpOutbox(){
  return establishFolder(pumpRoot(), "PumpOut");
}

function pumpOutboxTag(tag){
  return establishFolder(pumpOutbox(), tag);
}

function collectFiles(){
  var collection = [];
  var inbox = pumpInbox();
  var files = inbox.getFiles();
  while(files.hasNext()){
    var file = files.next();
    if(file.getName().indexOf(".pump") != -1){
      collection.push(file);
    }
  }
  return collection;
}

function extractTag(file){
  return file.getName().replace(".pump", "");
}

function processSingleFile(file, tag){
  var stamp = file.getDateCreated().toISOString();
  var name = stamp + "." + tag + ".jpg";
  var data = file.getBlob().getDataAsString();
  var blob = Utilities.newBlob(Utilities.base64Decode(data));
  blob.setContentType("image/jpeg");
  blob.setName(stamp + ".jpg");
  return blob;
}

function processAllFiles(collection){
  for(var i = 0; i < collection.length; i++){
    var tag = extractTag(collection[i]);
    var blob = processSingleFile(collection[i], tag);
    var folder = pumpOutboxTag(tag);
    folder.createFile(blob)
    collection[i].setTrashed(true);
  }
}

function run(){
  var collection = collectFiles();
  processAllFiles(collection);
}