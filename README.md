# Projrct Setup

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
5. `@app.route("/speech")` ใช้สำหรับ POST ข้อความเข้ามาเพื่เปลี่ยนเป็นเสียงแล้วส่งเสียงกลับไป

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
    <button type="button" class="btn btn-danger" style="display: none;" id="stop-btn"> หยุด
    </button>
    <div class="progress mx-auto my-3" style="max-width: 30rem;">
      <div class="progress-bar" role="progressbar" style="width: 0%;" aria-valuenow="0" aria-valuemin="0"
        aria-valuemax="10" id="sound"></div>
    </div>
  </div>
</div>
<div class="card text-center my-3 mx-auto" style="max-width: 50rem;">
  <div class="card-header">
    <h2 class="card-title"> ข้อความที่ได้ยิน </h2>
  </div>
  <div class="card-body text-start">
    <p id="content" class="card-text"></p>
  </div>
</div>

<div class="card text-center my-3 mx-auto" style="max-width: 50rem;">
  <div class="card-header">
    <h2 class="card-title">ผลลัพธ์</h2>
  </div>
  <div class="card-body">
    <div class="audio">
      <audio controls id="audio">
        <source src="" type="audio/x-wav">
      </audio>
    </div>
  </div>
</div>

<script type=text/javascript>
  // Define language to recognition
  let lang = "th-TH";

  // Set variable for stop watchsound
  var end = false;

  // Set up recognition
  var recognition = new webkitSpeechRecognition();
  recognition.lang = lang
  recognition.continuous = false;

  // Queries for common elements
  const contentEl = document.querySelector("#content");
  const startBtn = document.querySelector("#start-btn")
  const stopBtn = document.querySelector("#stop-btn")

  // On recognition have the result event
  recognition.onresult = function (event) {
    // Change inner display text element to recognition transcript
    contentEl.innerText = event.results[0][0].transcript
  }

  // On recognition start recognizes
  recognition.onstart = function () {
    end = false; // Set sound wave end to false
    watchSound(); // start watch sound wave
    startBtn.style.display = "none"; // Hide start button
    stopBtn.style.display = "initial"; // Show stop button
  }

  recognition.onend = function () {
    end = true; // Set sound wave end to true
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
    data.append("text", contentEl.innerText) // Append text to formdata

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

  // Function to watch sound frequency (Not matters)
  async function watchSound() {
    // Get display soundwave element
    const soundEl = document.querySelector('#sound');

    // Start audio stream
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
    const audioContext = new AudioContext();
    const mediaStreamAudioSourceNode = audioContext.createMediaStreamSource(stream);
    const analyserNode = audioContext.createAnalyser();
    mediaStreamAudioSourceNode.connect(analyserNode);
    const pcmData = new Float32Array(analyserNode.fftSize);

    // Get sound frequency and apply to display soundwave element
    const onFrame = () => {
      analyserNode.getFloatTimeDomainData(pcmData);
      let sumSquares = 0.0;
      for (const amplitude of pcmData) { sumSquares += amplitude*amplitude; } // Get sound amplitude
      let wave = Math.sqrt(sumSquares / pcmData.length) * 100 // Get wave frequency as percentage

      // Apply result to display soundwave element
      soundEl.style.width = `${wave*10}%`
      soundEl.setAttribute('aria-valuenow', wave)
      
      // On recognition end
      if (end) {
        stream.getTracks().forEach(function(track) {
          track.stop();
        });

        // Reset value of display soundwave element
        soundEl.style.width = `0%`
        soundEl.setAttribute('aria-valuenow', 0)
        return 
      }
      
      // Rewatch if recognition in not end
      window.requestAnimationFrame(onFrame);
    };

    // Start watch
    window.requestAnimationFrame(onFrame);
  }
</script>
{% endblock %}
```

#### Description
หน้านี้เป็นหน้าสำหรับ `@app.route('/speech_to_text')` โดยแสดงผลใน Block content ใน [templates/layout.html](templates/layout.html) ซึ่งจะแบ่งเป็น 3 card ดังนี้
1. **แปลงเสียงพูดเป็นข้อความ** - จะมีปุ่มกดเพื่อเริ่มอัดเสียงพูดแล้วแปลงเป็นข้อความ และจะมี progress bar เพื่อแสดงความถี่เสียงพูด
2. **ข้อความที่ได้ยิน** - มีไว้สำหรับแสดงผลข้อความที่เราพูดออกไป
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
      <audio controls id="audio">
        <source src="" type="audio/x-wav">
      </audio>
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
3.  **ผลลัพธ์** - มีไว้สำหรับแสดงผลลัพธ์สำหรับข้อความที่แปลงเป็นเสียงแล้ว

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

  // Set variable for stop watchsound
  var end = false;

  // Set up recognition
  var recognition = new webkitSpeechRecognition();
  recognition.lang = lang
  recognition.continuous = false;

  // Queries for common elements
  const contentEl = document.querySelector("#content");
  const startBtn = document.querySelector("#start-btn")
  const stopBtn = document.querySelector("#stop-btn")

  // On recognition have the result event
  recognition.onresult = function (event) {
    // Change inner display text element to recognition transcript
    contentEl.innerText = event.results[0][0].transcript
  }

  // On recognition start recognizes
  recognition.onstart = function () {
    end = false; // Set sound wave end to false
    watchSound(); // start watch sound wave
    startBtn.style.display = "none"; // Hide start button
    stopBtn.style.display = "initial"; // Show stop button
  }

  recognition.onend = function () {
    end = true; // Set sound wave end to true
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
    data.append("text", contentEl.innerText) // Append text to formdata

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

  // Function to watch sound frequency (Not matters)
  async function watchSound() {
    // Get display soundwave element
    const soundEl = document.querySelector('#sound');

    // Start audio stream
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
    const audioContext = new AudioContext();
    const mediaStreamAudioSourceNode = audioContext.createMediaStreamSource(stream);
    const analyserNode = audioContext.createAnalyser();
    mediaStreamAudioSourceNode.connect(analyserNode);
    const pcmData = new Float32Array(analyserNode.fftSize);

    // Get sound frequency and apply to display soundwave element
    const onFrame = () => {
      analyserNode.getFloatTimeDomainData(pcmData);
      let sumSquares = 0.0;
      for (const amplitude of pcmData) { sumSquares += amplitude*amplitude; } // Get sound amplitude
      let wave = Math.sqrt(sumSquares / pcmData.length) * 100 // Get wave frequency as percentage

      // Apply result to display soundwave element
      soundEl.style.width = `${wave*10}%`
      soundEl.setAttribute('aria-valuenow', wave)
      
      // On recognition end
      if (end) {
        stream.getTracks().forEach(function(track) {
          track.stop();
        });

        // Reset value of display soundwave element
        soundEl.style.width = `0%`
        soundEl.setAttribute('aria-valuenow', 0)
        return 
      }
      
      // Rewatch if recognition in not end
      window.requestAnimationFrame(onFrame);
    };

    // Start watch
    window.requestAnimationFrame(onFrame);
  }
</script>
```
#### Description
1. กำหนดภาษาที่ต้องการให้เปลี่ยนจากเสียงพูด
```javascript
// Define language to recognition
let lang = "th-TH";
```

2. กำหนดตัวแปร `end` เพื่อใช้สำหรับหยุดการตรวจจับคืนเสียงเมื่อพูดจบหรือหยุดการวิเคราะห์เสียง
```javascript
// Set variable for stop watchsound
var end = false;
```

3. สร้าง Object ในการวิเคราะห์เสียงพูด และตั้งค่าภาษาให้เป็นภาษาที่กำหนดไว้่จากตัวแปร `lang` ในข้อ 1 และตั้งค่า `continous` เป็น `false` เพื่อให้พูดจบหนึ่งประโยคแล้วเปลี่ยนเป็นเสียงพูดทันที ถ้าตั้งเป็น `true` มันจะฟังไปเรื่อยๆแล้วได้ยินที่ตัวเองพูดด้วยจะพูดซ้ำประโยคเดิมทั้งวัน
```javascript
// Set up recognition
var recognition = new webkitSpeechRecognition();
recognition.lang = lang
recognition.continuous = false;
```

4. ค้นหา element (el) ที่จำเป็นมาใช้ `content` คือ el ที่เอาไว้สำหรับแสดงข้อความที่ได้ยิน `startBtn` เป็น button ที่เอาไว้กดเริ่มอัดเสียง `stopBtn` เป็นปุ่มกดหยุดอัดเสียง
```javascript
// Queries for common elements
const contentEl = document.querySelector("#content");
const startBtn = document.querySelector("#start-btn")
const stopBtn = document.querySelector("#stop-btn")
```

5. อันนี้จะเป็นการตั้งค่าฟังก์ชันทุกครั้งที่เราเริ่มวิเคราะห์เสียง (Recognition) ฟังก์ชันนี้จะทำงาน โดยที่ `end = false` จะเป็นการทำให้ตัววัดคลื่นเสียงทำงาน `watchsound()` จะเป็นการเริ่มฟังคลื่นเสียง ถ้าเราไม่กำหนด `end = false` ก่อนฟังก์ชันนี้จะไม่ทำงาน ส่วนข้างล่างเมื่อเริ่มวิเคราะห์เสียงจะซ่อนปุ่ม `startBtn` และแสดงปุ่ม `stopBtn` ขึ้นมาแทน
```javascript
// On recognition start recognizes
recognition.onstart = function () {
  end = false; // Set sound wave end to false
  watchSound(); // start watch sound wave
  startBtn.style.display = "none"; // Hide start button
  stopBtn.style.display = "initial"; // Show stop button
}
```

6. อันนี้จะเป็นการตั้งค่าฟังก์ชันทุกครั้งที่วิเคราะห์เสียงเสร็จแล้ว (พูดจบประโยค) ฟังก์ชันนี้จะทำงาน โดยที่ `end = true` จะเป็นการทำให้ตัววัดคลื่นเสียง `watchsound()` ที่เริ่มตอนวิเคราะห์หยุดไปพร้อมกัน ถ้าเราไม่กำหนด `end = true` ฟังก์ชันนี้จะยังวัดระดับเสียงอยู่ ส่วนข้างล่างเมื่อวิเคราะห์เสียงเสร็จจะซ่อนปุ่ม `stopBtn` และแสดงปุ่ม `startBtn` ขึ้นมาแทน
```javascript
recognition.onend = function () {
  end = true; // Set sound wave end to true
  startBtn.style.display = "initial"; // Show start button
  stopBtn.style.display = "none"; // Hide stop button
  speak(); // Speak recognized text
}
```

7. เพิ่มการทำงานให้กับปุ่ม `startBtn` โดยที่เวลาคลิกจะเริ่มวิเคราะห์เสียง `recognition.start()` ซึ่งการทำงานในข้อ 5. จะทำงานหลังจากกดปุ่มนี้แล้วปุ่มนี้จะหายไปปุ่ม `stopBtn` จะขึ้นมาแทนเหมือนที่อะิบายในข้อ 5. ซึ่งปุ่ม `stopBtn` ที่ขึ้นมาแสดงแทนก็จะเพิ่มการทำงานเมื่อคลิกจะหยุดวิเคราะห์เสียงและจะทำงานในข้อที่หกสลับกันไปเรื่อยๆ
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

8. ฟังก์ชันนี้จะถูกเริ่มขึ้นหลักจากเราพูดจบหนึ่งประโยค(ดูข้อ 6.) ซึ่ง `url` จะเป็นการใช้ `url_for('speech')` คือการเรียกใช้ `@app.route('/speech')` ของ Flask หลังจากนั้นจะทำการสร้าง `formData` เพื่อส่งข้อมูล form ไปที่ `url` ซึ่งจะส่งข้อความไป ตรง `data.append("text", contentEl.innerText)` ก็คือเอาข้อความที่แสดงใน `contentEl` ที่เราแปลงเสียงเป็นแสดงนั่นแหละส่งไปผ่าน key ที่ชื่อว่า `"text"` และจะถูกเรียกใช้ใน [@app.route('/speech')](#@app.route('/speech')) ส่วน `fetch()` จะเป็นการส่งข้อมูลไปที่ `url` ของเรา ซึ่งเป็น `"method": "POST"` เหมือนที่เราตั้งค้าไว้ใน [@app.route('/speech')](#@app.route('/speech')) แล้วส่ง body เป็น `formData` ที่เราสร้างขึ้น จากนั้น `.then()` จะเป็นการเริ่มต้นการทำงานจริงๆ โดยที่ `.then()` อันแรกจะเริ่มส่งข้อมูลข้อความไปแล้วจะได้ `response` กลับมา แล้วใช้ `(response) => response.blob()` จะเป็นการเปลี่ยน `response` เป็น blob (สตริงอ็อบเจ็กต์ขนาดใหญ่ไบนารี) พูดง่าย ๆ ก็คือทำให้เป็นไฟล์ที่สามารถเล่นเป็นเสียงได้ แล้ว `.then()` ถัดไปจะเป็นการเอา blob ที่ถูงแปลงมาไปใช้ เราจะใช้ `FileReader()` ในการอ่าน blob ให้เป็น `dataURL` หรือเอาไฟล์ที่เล่นเป็นเสียงได้เปลี่ยนเป็น URL ที่เล่นได้อีกที (ยุ่งยากเนาะ) ส่วนข้างล่าง `document.getElementById("audio")` จะเป็นการดึง el ที่เอาไว้เล่นเสียงมา แล้วหยุดเสียง เปลี่ยน `src` เป็น URL ที่แปลงมา `load()` แล้ว `play()` เสียงทันที
```javascript
// Speak recognition text function
function speak() {
  let url = {{ url_for('speech')|tojson }} // URL for post text to route `speech` server

  // Create new formdata to send to server
  let data = new FormData()
  data.append("text", contentEl.innerText) // Append text to formdata

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

9. ส่วนอันนี้มันยาวมากขอไม่อธิบายก็คือบอกว่าไปหาเจอมาในเน็ตเป็นวิธีการอ่านค่าเสียงเป็นคลื่นเสียง Amplitude อ่านตาม comment ที่เขียนไว้ใน code ก็น่าจะได้
```javascript
// Function to watch sound frequency (Not matters)
async function watchSound() {
  // Get display soundwave element
  const soundEl = document.querySelector('#sound');

  // Start audio stream
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
  const audioContext = new AudioContext();
  const mediaStreamAudioSourceNode = audioContext.createMediaStreamSource(stream);
  const analyserNode = audioContext.createAnalyser();
  mediaStreamAudioSourceNode.connect(analyserNode);
  const pcmData = new Float32Array(analyserNode.fftSize);

  // Get sound frequency and apply to display soundwave element
  const onFrame = () => {
    analyserNode.getFloatTimeDomainData(pcmData);
    let sumSquares = 0.0;
    for (const amplitude of pcmData) { sumSquares += amplitude*amplitude; } // Get sound amplitude
    let wave = Math.sqrt(sumSquares / pcmData.length) * 100 // Get wave frequency as percentage

    // Apply result to display soundwave element
    soundEl.style.width = `${wave*10}%`
    soundEl.setAttribute('aria-valuenow', wave)
    
    // On recognition end
    if (end) {
      stream.getTracks().forEach(function(track) {
        track.stop();
      });

      // Reset value of display soundwave element
      soundEl.style.width = `0%`
      soundEl.setAttribute('aria-valuenow', 0)
      return 
    }
    
    // Rewatch if recognition in not end
    window.requestAnimationFrame(onFrame);
  };

  // Start watch
  window.requestAnimationFrame(onFrame);
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
อันนี้เหมือน ข้อ 9. ข้างบนเลยแค่เปลี่ยน `contentEl` เป็น `textEl` ที่เราใส่ข้อความไปแทน