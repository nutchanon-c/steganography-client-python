// console.log("decode");
const sg = require("any-steganography");
const fs = require("fs");
var args = process.argv;
function stegaDecode(inputFile, key) {
  const buffer = fs.readFileSync(inputFile);
  const message = sg.default.decode(buffer, "jpg", key);
  // console.log(message);
  // console.log("--------------------------------");
  return message;
}

console.log(stegaDecode("./1enc.jpg", "a".repeat(32)));
