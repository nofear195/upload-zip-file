
async function chunkDataStore(zipFileName, chunkData, chunkIndex) {
    const formData = new FormData()
    formData.append("zipFileName", zipFileName)
    formData.append("chunkData", chunkData)
    formData.append("chunkIndex", chunkIndex)

    const response = await axios({
        method: "post",
        url: '/chunk-data-store',
        data: formData,
        headers: { 'Content-Type': 'multipart/form-data' }
    })

    if (response.status !== 200) return { save: false, message: 'connect fail' }

    const resData = response.data
    if (!resData) return { save: false, message: resData.message }

    return { save: resData.data.save, message: resData.message }
}

async function dealWithUpload(zipFileName) {

    const reqData = { zipFileName }
    const response = await axios({
        method: "post",
        url: '/deal-with-upload',
        data: reqData,
        headers: { 'Content-Type': 'application/json' }
    })

    if (response.status !== 200) return { processing: false, message: 'connect fail' }

    const resData = response.data
    if (!resData) return { processing: false, message: resData.message }

    return { processing: resData.data.processing, message: resData.message }
}

async function getUploadImages(zipFileName) {

    const reqData = { zipFileName }
    const response = await axios({
        method: "post",
        url: '/upload-images',
        data: reqData,
        headers: { 'Content-Type': 'application/json' }
    })

    if (response.status !== 200) return []

    const resData = response.data
    if (!resData) return []

    return resData.data.image_content
}

async function savToDatabase(zipFileName) {

    const reqData = { zipFileName }
    const response = await axios({
        method: "post",
        url: '/save-to-database',
        data: reqData,
        headers: { 'Content-Type': 'application/json' }
    })

    if (response.status !== 200) return { save: false, message: 'connect fail' }

    const resData = response.data
    if (!resData) return { save: resData.data.save, message: resData.message }

    return {save: resData.data.save, message: resData.message }
}

async function dbInfo() {

    const response = await axios({
        method: "get",
        url: '/get-db-info',
        headers: { 'Content-Type': 'application/json' }
    })

    if (response.status !== 200) return { save: [], message: 'connect fail' }

    const resData = response.data
    if (!resData) return { dbData: [], message: resData.message }

    return {dbData: resData.data.db_data, message: resData.message }
}