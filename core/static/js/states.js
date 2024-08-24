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

      Alpine.data('window', ()=>({
         maximized: false, 
         width: 'max-w-2xl',
         open: true, 
         hiddenClass: '',
         toggleMaximize(){
            this.width = this.maximized ? 'max-w-2xl': 'max-w-full h-[calc(100%-1rem)] flex';
            this.maximized = !this.maximized;
         }, 
         close(){
            this.hiddenClass = this.open? 'hidden': ''; // if window is already open then it means we want to close it
            this.open = false; 
         }

      })); 

});


