
async function chunkDataStore(zipFileName,chunkData,chunkIndex) {
    const formData = new FormData()
    formData.append("zipFileName",zipFileName)
    formData.append("chunkData", chunkData)
    formData.append("chunkIndex",chunkIndex)

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
    return resData.data.save
}

async function dealWithUpload(zipFileName) {

    const reqData = {zipFileName}
    const response = await axios({
        method: "post",
        url: '/deal-with-upload',
        data:reqData,
        headers: { 'Content-Type': 'application/json' }
    })

    if (response.status !== 200) return

    const resData = response.data
    if (!resData) return

    console.log('response',resData)
    return resData.data.processing
}