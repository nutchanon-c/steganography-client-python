const sg = require("any-steganography");
const fs = require("fs");
var args = process.argv;
function stegaDecode(inputFile, key) {
  const buffer = fs.readFileSync(inputFile);
  const message = sg.default.decode(buffer, "jpg", key);
  process.stdout.write(message);
  return message;
}
var inputFile = args[2];
var key = args[3];

stegaDecode(inputFile, key);
