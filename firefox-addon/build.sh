cp -rf *.html build/
cp manifest.json build/

find . -name "*.js" -depth 1 -exec  uglifyjs  {} -o build/{} \;
find . -name "*.css" -depth 1 -exec  uglifycss  {} --output build/{} \;

#uglifyjs aiops.js -o build/aiops.js 
#uglifyjs content.js -o build/aiops.js 
#uglifyjs home.js -o build/aiops.js 
#uglifyjs option.js -o build/aiops.js 
#uglifyjs popup.js -o build/aiops.js 
#uglifycss home.css -o build/home.css 




