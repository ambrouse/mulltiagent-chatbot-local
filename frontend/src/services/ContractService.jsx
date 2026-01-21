import {axiosClient, axiosClientFile} from './axiosClient'


export async function LoadTemplateHome(){
    const a = await axiosClient.get("/contracts/load-template") 
    return a.data.result
}

export async function UploadTemplate(file){
    const formData = new FormData();
    formData.append("file", file);
    try{
        const a = await axiosClientFile.post("contracts/upload-contract", formData);
        return a.data.result
    }catch(e){
        alert(e.response.data.detail)
    }
}

export async function CreateFile(templateId, userInput, session){
    // if(templateId==""){
    //     alert("- Chưa chọn template!")
    //     return false
    // }
    // if(userInput==""){
    //     alert("- Không được để  rỗng input!")
    //     return false
    // }

    const requestData = {
        "user_id": "1",
        "session_id": session,
        "type_id": templateId,
        "user_input": userInput
        }
    // console.log(requestData)
    const a = await axiosClient.post("/contracts/create-contract", requestData );
    if(a.data.check){
        window.location.href = a.data.result;
        return a.data
    }else{
        return a.data
    }
}

export async function load_history(id_user, id_session){

    if(id_session==-1){return []}
   
    const requestData = {
        "user_id": "1",
        "session_id": id_session
        }

    // console.log(requestData, "0000000")
    const a = await axiosClient.post("/contracts/load_history", requestData );
    // console.log(a.data.result)
    return a.data.result
}


export async function delete_template(id_template){
   
    const a = await axiosClient.delete("/contracts/delete-template/"+id_template);
    // console.log(a.data.result)
    return a.data.result
}

export async function load_session(){
   
    const a = await axiosClient.get("/contracts/session/");
    return a.data.result
}

export async function delete_session(id){
   
    const a = await axiosClient.delete("/contracts/session/"+id);
    return a.data.result
}