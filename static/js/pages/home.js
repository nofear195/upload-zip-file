const app = Vue.createApp({
    data() {
        return {
            files: [],
        }
    },
    methods: {
        sliceFile: async function (file, chunkSize) {
            const totalSize = file.size;
            let chunks = [];
            let start = 0;
            let end = start + chunkSize

            while (start < totalSize) {
                let chunkSlice = await file.slice(start, end)
                chunks.push(chunkSlice)
                start = end
                end = end + chunkSize >= totalSize ? totalSize : end + chunkSize

            }
            return chunks
        },
        getFile: function (event) {
            this.files = event.target.files[0]
        },
        uploadFile: async function () {

            if (this.files.length === 0) return
            const chunkSize = 1024 * 10 * 10
            const chunks = await this.sliceFile(this.files, chunkSize)

            
            for (let i = 0; i < chunks.length; i++) {
                await chunkDataStore(chunks[i], i)
            }
            const interval = setInterval(async () => {
                const result = await dealWithUpload()
                if (result) clearInterval(interval)
            }, 5000)

        },
        checkUpload: async function () {

        },
    },
})

const vm = app.mount('#app');