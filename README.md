# Project Setup

## Set up venv
```
py -m venv venv
```

## Activate venve
```
venv\Scripts\activate
```

## install dependencies
```
pip install Flask
// or
py -m pip install Flask
```

```
pip install gTTS
// or
py -m pip install gTTS
```

## run project
```
python main.py
```

# Project information
Flask ที่เราใช้มันจะเป็น server application สำหรับ back-end (หลังบ้าน) หรือส่วนการทำงาน ถ้าต้องการบันทึกเสียงอะไรต่างๆต้องมีการใช้ JavaScript มาใช้ช่วยในการอัดเสียงหรือฟังก์ชันต่างๆสำหรับ front-end (หน้าบ้าน) หรือส่วนที่แสดงให้ผู้ใช้เห็นถึงจะใช้งานได้

# UPDATE*

## speech_to_text.html
1. ลบฟังก์ชันสำหรับวัดค่าเสียงออกไป เพราะว่ามันค่อนข้างกินทรัพยากรเครื่องเยอะทำให้เว็บไม่ยอมแปลงเสียงพูดสักที แล้วเพิ่มฟังก์ชัน `recognition.interimResults = true;` เข้ามาแทน เพื่อที่จะให้ตัววิเคราะห์เสียงแปลงเป็นคำพูดทุกๆคำแทนโดยที่ไม่ต้องรอให้จบประโยค (การเปลี่ยนเสียงเป็นเสียงยังทำหลังจากจบประโยคเหมือนเดิมเพียงเค่กล่องข้อความจะแสดงคำต่อคำที่พูดเท่านั้น) 
2. ได้มีการเพิ่มทางเลือก `window.SpeechRecognition` กับ `window.webkitSpeechRecognition` จะให้เครื่องค้นหาตัววิเคราะห์เสียงระหว่างสองอันนี้ ถ้าเครื่องไม่เจอสักอันจะวิเครสะห์เสียงไม่ได้
3. มีการแก้ไข UI ให้เหมาะกับการเปลี่ยนแปลงใน 2 ข้อแรก

# File description

## main.py

```python
from flask import Flask, render_template, request, Response, redirect
from gtts import gTTS

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/text_to_speech")
def text_to_speech():
    return render_template("text_to_speech.html")


@app.route("/speech_to_text")
def speech_to_text():
    return render_template("speech_to_text.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/speech", methods=["POST"])
def speech():
    # Function to generate speech audio to response
    def generate():
        with open(f"./static/speech.mp3", "rb") as file:
            data = file.read(1024)
            while data:
                yield data
                data = file.read(1024)
    
    text = request.form.get("text") # Get text from formData
    filename = "speech.mp3" # Set filename
    tts = gTTS(text, lang="th") # Setup gTTS
    tts.save(f"./static/{filename}") # Save gTTS to file
    return Response(generate(), mimetype="audio/x-wav") # Return Response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
```

#### Description
1. `@app.route("/")` ใช้สำหรับแสดงผลไฟล์ [templates/index.html](templates/index.html)
2. `@app.route("/text_to_speech")` ใช้สำหรับแสดงผลไฟล์ [templates/text_to_speech.html](templates/text_to_speech.html)
3. `@app.route("/speech_to_text")` ใช้สำหรับแสดงผลไฟล์ [templates/speech_to_text.html](templates/speech_to_text.html)
4. `@app.route("/about")` ใช้สำหรับแสดงผลไฟล์ [templates/about.html](templates/about.html)
5. `@app.route("/speech")` ใช้สำหรับ POST ข้อความเข้ามาเพื่อเปลี่ยนเป็นเสียงแล้วส่งเสียงกลับไป

## Templates

### index.html
```html
{% extends "layout.html" %}

{% block content %}
<div class="row">
  <div class="col-12">
    <div class="card mt-5 mb-2">
      <div class="card-header">
        Feature
      </div>
      <div class="card-body">
        <h2 class="card-title">
          แปลงข้อความเป็นเสียงพูด
        </h2>
        <a class="btn btn-success" href="{{ url_for('text_to_speech') }}"> ทดลอง </a>
      </div>
    </div>
  </div>
  <div class="col-12">
    <div class="card my-2">
      <div class="card-header">
        Feature
      </div>
      <div class="card-body">
        <h2 class="card-title">
          แปลงเสียงพูดเป็นข้อความ
        </h2>
        <a class="btn btn-success" href="{{ url_for('speech_to_text') }}"> ทดลอง </a>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

#### Description
หน้านี้เป็นหน้าหลักที่แสดงใน `@app.route('/')` โดยแสดงผลใน Block content ใน [templates/layout.html](templates/layout.html) ซึ่งจะใช้ card ใน bootstrap เพื่อแสดงผลรายการ ซึ่งแต่ละรายการจะมีปุ่มกดเข้าไปในหน้าของรายการนั้นอีกที

### speech_to_text.html

```html
{% extends 'layout.html' %}

{% block content %}
<div class="card text-center my-3 mx-auto" style="max-width: 50rem;">
  <div class="card-header">
    <h2 class="card-title">แปลงเสียงพูดเป็นข้อความ</h2>
  </div>
  <div class="card-body">
    <button type="button" class="btn btn-success" id="start-btn"> ฟังเสียง </button>
    <button type="button" class="btn btn-danger" style="display: none;" id="stop-btn"> หยุด </button>
    <div class="form-group text-start">
      <div class="mb-3 mx-auto" style="max-width: 40rem;">
        <label for="content">ข้อความที่ได้ยิน</label>
        <textarea class="form-control" id="content" rows="3" disabled readonly></textarea>
      </div>
    </div>
  </div>
</div>

<div class="card text-center my-3 mx-auto" style="max-width: 50rem;">
  <div class="card-header">
    <h2 class="card-title">ผลลัพธ์</h2>
  </div>
  <div class="card-body">
    <div class="audio">
      <audio controls id="audio"></audio>
    </div>
  </div>
</div>

<script type=text/javascript>
  // Define language to recognition
  let lang = "th-TH";

  // Set up recognition
  var Recognition = window.SpeechRecognition || window.webkitSpeechRecognition
  var recognition = new Recognition();
  recognition.lang = lang
  recognition.continuous = false;
  recognition.interimResults = true;

  // Queries for common elements
  const contentEl = document.querySelector("#content");
  const startBtn = document.querySelector("#start-btn")
  const stopBtn = document.querySelector("#stop-btn")

  // On recognition have the result event
  recognition.onresult = function (event) {
    // Change inner display text element to recognition transcript
    contentEl.value = Object.values(event.results).map(value => value[0].transcript).join("")
  }

  // On recognition start recognizes
  recognition.onstart = function () {
    startBtn.style.display = "none"; // Hide start button
    stopBtn.style.display = "initial"; // Show stop button
  }

  recognition.onend = function () {
    startBtn.style.display = "initial"; // Show start button
    stopBtn.style.display = "none"; // Hide stop button
    speak(); // Speak recognized text
  }

  // Add start button on click event
  startBtn.addEventListener('click', function start(event) {
    recognition.start(); // Start recognizer `recognition.onstart` will be called
  })

  // Add stop button onclick event
  stopBtn.addEventListener('click', function stop(event) {
    recognition.stop(); // Stop recognizer `recognition.onend` will be called
  })

  // Speak recognition text function
  function speak() {
    let url = {{ url_for('speech')|tojson }} // URL for post text to route `speech` server

    // Create new formdata to send to server
    let data = new FormData()
    data.append("text", contentEl.value) // Append text to formdata

    // Send data to server
    fetch(url, { "method": "POST", "body": data })
      .then((response) => response.blob()) // change response to blob
      .then((blob) => {
        // Reab blob to data url for playing
        var reader = new FileReader(); 
        reader.readAsDataURL(blob); 

        // On blob loaded
        reader.onloadend = function() {
          var src = reader.result; // Audio source  
          document.getElementById("audio").pause() // Stop playing audio, if audio is playing
          document.getElementById("audio").setAttribute('src', src) // Set audio player source to reader result
          document.getElementById("audio").load() // Let audio player load source
          document.getElementById("audio").play() // Play audio 
        }
      })
  }
</script>
{% endblock %}
```

#### Description 
หน้านี้เป็นหน้าสำหรับ `@app.route('/speech_to_text')` โดยแสดงผลใน Block content ใน [templates/layout.html](templates/layout.html) ซึ่งจะแบ่งเป็น 3 card ดังนี้
1. **แปลงเสียงพูดเป็นข้อความ** - จะมีปุ่มกดเพื่อเริ่มอัดเสียงพูดแล้วแปลงเป็นข้อความ และจะมีกล่องข้อความแสดงคำพูดที่ได้ยินข้างในอีกที
3.  **ผลลัพธ์** - มีไว้สำหรับแสดงผลลัพธ์สำหรับเสียงที่แปลงไปแล้ว

### text_to_speech.html

```html
{% extends "layout.html" %}

{% block content %}
<div class="card text-center my-3 mx-auto" style="max-width: 50rem;">
  <div class="card-header">
    <h2 class="card-title">แปลงข้อความเป็นเสียงพูด</h2>
  </div>
  <div class="card-body">
    <div class="form-group text-start">
      <div class="mb-3 mx-auto" style="max-width: 40rem;">
        <label for="text" class="form-label">ใส่ข้อความ</label>
        <textarea class="form-control" id="text" rows="3" name="text"></textarea>
      </div>
    </div>
    <button id="start-btn" class="btn btn-success" onclick="speak()">แปลงเสียง</button>
  </div>
</div>
<div class="card text-center my-3 mx-auto" style="max-width: 50rem;">
  <div class="card-header">
    <h2 class="card-title">ผลลัพธ์</h2>
  </div>
  <div class="card-body">
    <div class="audio">
      <audio controls id="audio"></audio>
    </div>
  </div>
</div>

<script type=text/javascript>
  // Speak text function
  function speak() {
    const textEl = document.querySelector("#text"); // Get text element
    let url = {{ url_for('speech')|tojson }} // URL for post text to route `speech` server

    // Create new formdata to send to server
    let data = new FormData()
    data.append("text", textEl.value) // Append text to formdata

    // Send data to server
    fetch(url, { "method": "POST", "body": data })
      .then((response) => response.blob()) // change response to blob
      .then((blob) => {
        // Reab blob to data url for playing
        var reader = new FileReader(); 
        reader.readAsDataURL(blob); 

        // On blob loaded
        reader.onloadend = function() {
          var src = reader.result; // Audio source  
          document.getElementById("audio").pause() // Stop playing audio, if audio is playing
          document.getElementById("audio").setAttribute('src', src) // Set audio player source to reader result
          document.getElementById("audio").load() // Let audio player load source
          document.getElementById("audio").play() // Play audio 
        }
      })
  }
</script>
{% endblock %}
```
#### Description
หน้านี้เป็นหน้าสำหรับ `@app.route('/text_to_speech')` โดยแสดงผลใน Block content ใน [templates/layout.html](templates/layout.html) ซึ่งจะแบ่งเป็น 2 card ดังนี้
1. **แปลงข้อความเป็นเสียงพูด** - ข้างในจะมี `<textarea></textarea>` สำหรับใส่ข้อความที่ต้องการแปลงเป็นเสียงพูดลงไป และมี button สำหรับยืนยันการเปลี่ยนข้อความเป็นเสียงพูด
2.  **ผลลัพธ์** - มีไว้สำหรับแสดงผลลัพธ์สำหรับข้อความที่แปลงเป็นเสียงแล้ว

# Function

## @app.route("/speech")

```python
@app.route("/speech", methods=["POST"])
def speech():
    # Function to generate speech audio to response
    def generate():
        with open(f"./static/speech.mp3", "rb") as file:
            data = file.read(1024)
            while data:
                yield data
                data = file.read(1024)
    
    text = request.form.get("text") # Get text from formData
    filename = "speech.mp3" # Set filename
    tts = gTTS(text, lang="th") # Setup gTTS
    tts.save(f"./static/{filename}") # Save gTTS to file
    return Response(generate(), mimetype="audio/x-wav") # Return Response
```
#### Description
1. ใน route นี้ จะมีการกำหนด `methods=["POST"]` เพื่อใช้สำหรับ POST เท่านั้น 
2. ข้างในจะมี function `generate` เพื่ออ่านไฟล์ข้อความที่เปลี่ยนเป็นเสียงแล้วซึ่งจะถูกใช้ตรง `return Response(generate(), mimetype="audio/x-wav")`
3. `text = request.form.get("text")` จะทำการรับค่าข้อความที่ถูกส่งมา (POST)
4. ที่เหลือจะใช้ gTTS (google text to speech) เพื่อเปลี่ยนข้อความที่รับค่ามาเป็นเสียงพูดแล้วส่งกลับไปต้นทางที่ POST เข้ามาด้วยฟังก์ชัน `generate` ใน type `"audio/x-wav"`

## srcipt ใน speech_to_text.html
```html
<script type=text/javascript>
  // Define language to recognition
  let lang = "th-TH";

  // Set up recognition
  var Recognition = window.SpeechRecognition || window.webkitSpeechRecognition
  var recognition = new Recognition();
  recognition.lang = lang
  recognition.continuous = false;
  recognition.interimResults = true;

  // Queries for common elements
  const contentEl = document.querySelector("#content");
  const startBtn = document.querySelector("#start-btn")
  const stopBtn = document.querySelector("#stop-btn")

  // On recognition have the result event
  recognition.onresult = function (event) {
    // Change inner display text element to recognition transcript
    contentEl.value = Object.values(event.results).map(value => value[0].transcript).join("")
  }

  // On recognition start recognizes
  recognition.onstart = function () {
    startBtn.style.display = "none"; // Hide start button
    stopBtn.style.display = "initial"; // Show stop button
  }

  recognition.onend = function () {
    startBtn.style.display = "initial"; // Show start button
    stopBtn.style.display = "none"; // Hide stop button
    speak(); // Speak recognized text
  }

  // Add start button on click event
  startBtn.addEventListener('click', function start(event) {
    recognition.start(); // Start recognizer `recognition.onstart` will be called
  })

  // Add stop button onclick event
  stopBtn.addEventListener('click', function stop(event) {
    recognition.stop(); // Stop recognizer `recognition.onend` will be called
  })

  // Speak recognition text function
  function speak() {
    let url = {{ url_for('speech')|tojson }} // URL for post text to route `speech` server

    // Create new formdata to send to server
    let data = new FormData()
    data.append("text", contentEl.value) // Append text to formdata

    // Send data to server
    fetch(url, { "method": "POST", "body": data })
      .then((response) => response.blob()) // change response to blob
      .then((blob) => {
        // Reab blob to data url for playing
        var reader = new FileReader(); 
        reader.readAsDataURL(blob); 

        // On blob loaded
        reader.onloadend = function() {
          var src = reader.result; // Audio source  
          document.getElementById("audio").pause() // Stop playing audio, if audio is playing
          document.getElementById("audio").setAttribute('src', src) // Set audio player source to reader result
          document.getElementById("audio").load() // Let audio player load source
          document.getElementById("audio").play() // Play audio 
        }
      })
  }
</script>
```
#### Description
1. กำหนดภาษาที่ต้องการให้เปลี่ยนจากเสียงพูด
```javascript
// Define language to recognition
let lang = "th-TH";
```

2. สร้าง Object ในการวิเคราะห์เสียงพูดซึ่งจะเลือกระหว่าง `window.SpeechRecognition` กับ `window.webkitSpeechRecognition` ถ้าอันแรกเครื่องไม่มีจะไปอันถัดไป ถ้าไม่มีเลยก็จะ ERROR จากนั้นก็ตั้งค่าภาษาให้เป็นภาษาที่กำหนดไว้จากตัวแปร `lang` ในข้อ 1 และตั้งค่า `continuous` เป็น `false` เพื่อให้พูดจบหนึ่งประโยคแล้วเปลี่ยนเป็นเสียงพูดทันที ถ้าตั้งเป็น `true` มันจะฟังไปเรื่อยๆแล้วได้ยินที่ตัวเองพูดด้วยจะพูดซ้ำประโยคเดิมทั้งวัน ส่วน `interimResults` จะเป็นการทำให้วิเคราะห์ทุกคำไปเรื่อยๆจนจบหนึ่งประโยคแล้วค่อยแปลงเป็นเสียง ถ้าตั้งค่าเป็น `false` ในกล่องข้อความที่ได้ยินจะขึ้นหลังจบประโยคแต่อันนี้จะจะขึ้นทีละคำต่อกันเลย
```javascript
// Set up recognition
var Recognition = window.SpeechRecognition || window.webkitSpeechRecognition
var recognition = new Recognition();
recognition.lang = lang
recognition.continuous = false;
recognition.interimResults = true;
```

3. นำ element (el) ที่เกี่ยวข้องมาใช้งาน โดยที่ `content` คือ el ที่เอาไว้สำหรับแสดงข้อความที่ได้ยิน `startBtn` เป็น button ที่เอาไว้กดเริ่มอัดเสียง `stopBtn` เป็นปุ่มกดหยุดอัดเสียง
```javascript
// Queries for common elements
const contentEl = document.querySelector("#content");
const startBtn = document.querySelector("#start-btn")
const stopBtn = document.querySelector("#stop-btn")
```

4. อันนี้จะเป็นการตั้งค่าฟังก์ชันทุกครั้งที่เราเริ่มวิเคราะห์เสียง (Recognition) ฟังก์ชันนี้จะทำงาน โดยที่เมื่อเริ่มวิเคราะห์เสียงจะซ่อนปุ่ม `startBtn` และแสดงปุ่ม `stopBtn` ขึ้นมาแทน
```javascript
// On recognition start recognizes
recognition.onstart = function () {
  startBtn.style.display = "none"; // Hide start button
  stopBtn.style.display = "initial"; // Show stop button
}
```

5. อันนี้จะเป็นการตั้งค่าฟังก์ชันทุกครั้งที่วิเคราะห์เสียงเสร็จแล้ว (พูดจบประโยค) ฟังก์ชันนี้จะทำงาน โดยที่เมื่อวิเคราะห์เสียงเสร็จจะซ่อนปุ่ม `stopBtn` และแสดงปุ่ม `startBtn` ขึ้นมาแทน
```javascript
recognition.onend = function () {
  startBtn.style.display = "initial"; // Show start button
  stopBtn.style.display = "none"; // Hide stop button
  speak(); // Speak recognized text
}
```

6. เพิ่มการทำงานให้กับปุ่ม `startBtn` โดยที่เวลาคลิกจะเริ่มวิเคราะห์เสียง `recognition.start()` ซึ่งการทำงานในข้อ 4. จะทำงานหลังจากกดปุ่มนี้แล้วปุ่มนี้จะหายไปปุ่ม `stopBtn` จะขึ้นมาแทนเหมือนที่อธิบายในข้อ 5. ซึ่งปุ่ม `stopBtn` ที่ขึ้นมาแสดงแทนก็จะเพิ่มการทำงานเมื่อคลิกจะหยุดวิเคราะห์เสียงและจะทำงานในข้อที่หกสลับกันไปเรื่อยๆ
```javascript
// Add start button on click event
startBtn.addEventListener('click', function start(event) {
  recognition.start(); // Start recognizer `recognition.onstart` will be called
})

// Add stop button onclick event
stopBtn.addEventListener('click', function stop(event) {
  recognition.stop(); // Stop recognizer `recognition.onend` will be called
})
```

7. ฟังก์ชันนี้จะถูกเริ่มขึ้นหลักจากเราพูดจบหนึ่งประโยค(ดูข้อ 5.) ซึ่ง `url` จะเป็นการใช้ `url_for('speech')` คือการเรียกใช้ `@app.route('/speech')` ของ Flask หลังจากนั้นจะทำการสร้าง `formData` เพื่อส่งข้อมูล form ไปที่ `url` ซึ่งจะส่งข้อความไป ตรง `data.append("text", contentEl.value)` ก็คือเอาข้อความที่แสดงใน `contentEl` ที่เราแปลงเสียงไปแสดงนั่นแหละส่งไปผ่าน key ที่ชื่อว่า `"text"` และจะถูกเรียกใช้ใน [@app.route('/speech')](#@app.route('/speech')) ส่วน `fetch()` จะเป็นการส่งข้อมูลไปที่ `url` ของเรา ซึ่งเป็น `"method": "POST"` เหมือนที่เราตั้งค้าไว้ใน [@app.route('/speech')](#@app.route('/speech')) แล้วส่ง body เป็น `formData` ที่เราสร้างขึ้น จากนั้น `.then()` จะเป็นการเริ่มต้นการทำงานจริงๆ โดยที่ `.then()` อันแรกจะเริ่มส่งข้อมูลข้อความไปแล้วจะได้ `response` กลับมา แล้วใช้ `(response) => response.blob()` จะเป็นการเปลี่ยน `response` เป็น blob (สตริงอ็อบเจ็กต์ขนาดใหญ่ไบนารี) พูดง่าย ๆ ก็คือทำให้เป็นไฟล์ที่สามารถเล่นเป็นเสียงได้ แล้ว `.then()` ถัดไปจะเป็นการเอา blob ที่ถูกแปลงมาไปใช้ เราจะใช้ `FileReader()` ในการอ่าน blob ให้เป็น `dataURL` หรือเอาไฟล์ที่เล่นเป็นเสียงได้เปลี่ยนเป็น URL ที่เล่นได้อีกที (ยุ่งยากเนาะ) ส่วนข้างล่าง `document.getElementById("audio")` จะเป็นการดึง el ที่เอาไว้เล่นเสียงมา แล้วหยุดเสียง เปลี่ยน `src` เป็น URL ที่แปลงมา `load()` แล้ว `play()` เสียงทันที
```javascript
// Speak recognition text function
function speak() {
  let url = {{ url_for('speech')|tojson }} // URL for post text to route `speech` server

  // Create new formdata to send to server
  let data = new FormData()
  data.append("text", contentEl.value) // Append text to formdata

  // Send data to server
  fetch(url, { "method": "POST", "body": data })
    .then((response) => response.blob()) // change response to blob
    .then((blob) => {
      // Reab blob to data url for playing
      var reader = new FileReader(); 
      reader.readAsDataURL(blob); 

      // On blob loaded
      reader.onloadend = function() {
        var src = reader.result; // Audio source  
        document.getElementById("audio").pause() // Stop playing audio, if audio is playing
        document.getElementById("audio").setAttribute('src', src) // Set audio player source to reader result
        document.getElementById("audio").load() // Let audio player load source
        document.getElementById("audio").play() // Play audio 
      }
    })
}
```

## Script ใน text_to_speech.html
```html
<script type=text/javascript>
  // Speak text function
  function speak() {
    const textEl = document.querySelector("#text"); // Get text element
    let url = {{ url_for('speech')|tojson }} // URL for post text to route `speech` server

    // Create new formdata to send to server
    let data = new FormData()
    data.append("text", textEl.value) // Append text to formdata

    // Send data to server
    fetch(url, { "method": "POST", "body": data })
      .then((response) => response.blob()) // change response to blob
      .then((blob) => {
        // Reab blob to data url for playing
        var reader = new FileReader(); 
        reader.readAsDataURL(blob); 

        // On blob loaded
        reader.onloadend = function() {
          var src = reader.result; // Audio source  
          document.getElementById("audio").pause() // Stop playing audio, if audio is playing
          document.getElementById("audio").setAttribute('src', src) // Set audio player source to reader result
          document.getElementById("audio").load() // Let audio player load source
          document.getElementById("audio").play() // Play audio 
        }
      })
  }
</script>
```

#### Description
อันนี้เหมือน ข้อ 7. ข้างบนเลยแค่เปลี่ยน `contentEl` เป็น `textEl` ที่เราใส่ข้อความไปแทน
