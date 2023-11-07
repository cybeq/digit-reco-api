<template>
  <div class="flex-container">
    <vue-drawing-canvas  :outputHeight="28" :outputWidth="28" style="border:solid 2px black" :line-width="2" :width="50" :height="50" ref="VueCanvasDrawing" />
    <button @click="recognizeLetter">Rozpoznaj Cyrfę</button>
    <div>
      {{prediction}}
    </div>
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
      prediction:null

    };
  },
  methods: {
   async recognizeLetter() {
      const formData = new FormData();

      const canvas = document.querySelector('#VueDrawingCanvas');
      const imageData = canvas.toDataURL();
      const blob = await fetch(imageData).then(res => res.blob());

      formData.append('file', blob, 'image.png');

      this.service.getPrediction(formData).then(res => {
        this.prediction = res.data?.prediction
        this.$refs.VueCanvasDrawing.reset()
      });
    },
  },
  async created() {
  },
};
</script>
<style>
.flex-container{
  width:100vw;
  height:100vh;
  display:flex;
  justify-content: center;
  align-items:center;
  button{
  height: 54px;
    border-radius:0;
    border:solid 2px black;
  }
  div{
    display:flex;
    justify-content: center;
    align-items: center;
    width:50px;
    height:50px;
  }
}

</style>