
async function chunkDataStore(chunkData,chunkIndex) {
    const formData = new FormData()
    formData.append("chunkData", chunkData)
    formData.append("chunkIndex",chunkIndex)

    console.log('formdat',chunkData.size)
    const response = await axios({
        method: "post",
        url: '/chunk-data-store',
        data: formData,
        headers: { 'Content-Type': 'multipart/form-data' }
    })

    if (response.status !== 200) return

    const resData = response.data
    if (!resData) return

    console.log('response',resData)
}

async function dealWithUpload() {

    const response = await axios({
        method: "post",
        url: '/deal-with-upload',
        headers: { 'Content-Type': 'application/json' }
    })

    if (response.status !== 200) return

    const resData = response.data
    if (!resData) return

    console.log('response',resData)
}