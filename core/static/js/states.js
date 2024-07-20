document.addEventListener('alpine:init', ()=>{
    Alpine.data('navImage', ()=>({
        url:undefined,
        loaded: false,
        init(){
          this.getImage();
        }, 

        async getImage(){
            const response = await fetch('https://avatars.githubusercontent.com/u/98283377?v=4');
            const blob = await response.blob();
            this.url = URL.createObjectURL(blob);
            this.loaded = true;
          }
      })); 

      Alpine.data('uploadForm', ()=>({
         filename:'Choose a file', 
         changed: false, 
         async toggle(){
            this.filename = document.getElementById('dropzone-file').files[0].name;
            const response = await fetch('/get-icon/?filename=' + this.filename);
            const svg = await response.text();
            const iconDiv = document.getElementById('svg-icon');
            // * template could not be modified continiously for some reason so I had to use this method
            iconDiv.innerHTML = `
              <template x-if="changed">
                  ${svg}
               </template>
            `
            this.changed = true;
         }

      })); 
});


