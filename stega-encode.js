// console.log("encode");
const sg = require("any-steganography");
const fs = require("fs");
var args = process.argv;
function stegaEncode(guestFile, message, outputFile, key) {
    const buffer = sg.default.write(guestFile, message, key);
    fs.writeFile(outputFile, buffer, (err) => {
        if (err) {
            console.log(err);
            return;
        }
    });
    return;
}

const file = args[2];
const message = args[3];
const key = args[4];
// var filename = file.replace(/^.*[\\\/]/, '')
const filename = args[5];
stegaEncode(
  file,
  message,
  `./output/${filename.split(".")[0]}.enc.${filename.split(".")[1]}`,
  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
);
