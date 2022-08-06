function submit(code, id){
    dataJson = {"code": code, "problem_id": id};
    $.ajax({
        url: "/submit",
        type: "POST",
        data: JSON.stringify(dataJson),
        dataType: "json",
        contentType: "application/json",
        success(data, status, xhr){
            return data;
        }
    })
}