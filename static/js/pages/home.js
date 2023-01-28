const app = Vue.createApp({
    data() {
        return {
            files: [],
            progress: 0,
            currentStatus: false,
            currentMessage: '',
            uploadImages: [],
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

            this.progress = 0
            this.uploadImages = []
            if (this.files.length === 0) return
            const chunkSize = 1024 * 10
            const chunks = await this.sliceFile(this.files, chunkSize)

            const zipFileName = this.files.name
            for (let i = 0; i < chunks.length; i++) {
                const { save, message } = await chunkDataStore(zipFileName, chunks[i], i)
                this.currentStatus = save
                this.currentMessage = message
                if (!save) return
                this.progress = ((i + 1) / chunks.length) * 100
            }
            const interval = setInterval(async () => {
                const { processing, message } = await dealWithUpload(zipFileName)
                this.currentStatus = processing
                this.currentMessage = message
                if (processing) {
                    clearInterval(interval)
                    const getUploadImage = await getUploadImages(zipFileName)
                    if (getUploadImage.length === 0) return
                    this.uploadImages = getUploadImage
                }
            }, 5000)


        },
    },
})

const vm = app.mount('#app');