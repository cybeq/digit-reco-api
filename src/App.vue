<template>
  <div class="flex-container">
    <main>
      <section class="header">
        <div style="display:flex; align-items: center">
              <input type="checkbox" v-model="options.quickDraw" />
               <span>Wyczyść i rozpoznaj po narysowaniu</span>
        </div>
        <div style="text-align:right">
           <button @click="recognizeLetter">Rozpoznaj Cyrfę</button>
        </div>

      </section>
      <section class="drawing-ctx">
        <vue-drawing-canvas  :outputHeight="28" :outputWidth="28" style=" border:solid 2px #00000040;" :line-width="12" :width="200" :height="200" ref="VueCanvasDrawing" />
        <div class="prediction-result">
          <section class="prediction">
            Prediction: {{prediction}}
          </section>
        </div>
      </section>

    </main>
  </div>
</template>

<script>
import VueDrawingCanvas from "vue-drawing-canvas";
import * as tf from "@tensorflow/tfjs";
import axios from "axios";

export default {
  name: "App",
  components: {
    VueDrawingCanvas,
  },
  setup(){
    const ServiceClass = class {
      URL = "http://localhost:8000"
      async getPrediction(formData){
        return await axios.post(`${this.URL}/`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }}
        );

      }
      async getLoss(){
        return await axios.get(`${URL}/loss`)
      }
    }
    return {ServiceClass}
  },
  data() {
    return {
      model: null,
      service:new this.ServiceClass(),
      prediction:null,
      options:{
        quickDraw:true
      }

    };
  },
  methods: {
   async recognizeLetter() {
      const formData = new FormData();

      const canvas = document.querySelector('#VueDrawingCanvas');
      const imageData = canvas.toDataURL();
      const blob = await fetch(imageData).then(res => res.blob());

      formData.append('file', blob, 'image.png');
      this.prediction = '⏳'
      this.service.getPrediction(formData).then(res => {
        this.prediction = res.data?.prediction
        this.$refs.VueCanvasDrawing.reset()
      }).catch(e=> {
        this.prediction = 'E!'; console.log(e)
      });
    },
  },
  async created() {
    var drawing = false;
    this.$nextTick(()=>{
      const canvas = document.querySelector('#VueDrawingCanvas');
      canvas.addEventListener('mousedown',()=>{
        if(!this.options.quickDraw) return;

        drawing = true;
      })
      canvas.addEventListener('mouseup',()=>{
        if(!this.options.quickDraw) return;
        if(drawing){
          this.recognizeLetter()
          drawing = false;
        }
      })
    })

  },
};
</script>
<style>
@font-face {
  font-family: "Robot";
  src: url("@/assets/Roboto-Medium.ttf");
}
body{
  background: #70788d;
  font-family: "Roboto", sans-serif!important;
  overflow:hidden
}
.flex-container{
  width:100vw;
  height:100vh;
  display:flex;
  justify-content: center;
  align-items:center;
  box-sizing: border-box;
  main{
    width:60vw;
    height:70vh;
    min-height: 300px;
    box-sizing: border-box;
    min-width:800px;
    max-height:300px;
    background:white;
    padding: 8px;
    color: #70788d;
    box-shadow:3px 3px 3px #00000030;
    .header{
      width:100%;
      border-bottom: solid 2px #fc716a;
      height:30px;
      background:#00000020;
      font-size:0.8em;
      display:grid;
      grid-template-columns: 1fr 1fr;
      box-sizing: border-box;

    }
    .drawing-ctx{
      padding-block:12px;
    }
  }
  button{
    border:solid 2px #00000030;
    border-radius:0;
    border-left: solid 3px #00000030;
    border-right: solid 3px #00000030;
    width:200px;
    height:30px;
    background:#fc716a;
    color:#fff;
  }
  .prediction-result{


  }
}
.drawing-ctx{
  display:flex;
  gap: 20px;
}
</style>