const sio =io( {
     transportOptions :{
        polling: {
            extraHeaders:{
                'X-Username': window.prompt("Whats Your name?")
                //'X-Authtoken': window.prompt("Enter AuthToken:")
            }
        } 
   } 
    
});


sio.on('connect',() => {
    var user_nm ;

    console.log("connected")
    //user_nm = window.prompt("Whats Your name?")
    
    sio.emit('greet', {"user": user_nm});
    
    });
 


// Client reciving the greeet response
sio.on('rsp_greet',(data) => {
    console.log(data['msg'])
    solution_name = window.prompt(data['msg'])
    console.log("you entered ", solution_name)
    sio.emit('get_soln_nm', {"soln_name": solution_name});
});


sio.on('rsp_soln_name', (data) => {
    console.log(data['msg'])
    ind_cat = window.prompt(data['msg'])
    console.log("you entered ", ind_cat)
    sio.emit('get_ind_cat', {"ind_cat": ind_cat});
});


sio.on('rsp_industry_cat', (data) => {
    console.log(data['msg'])
    func_area = window.prompt(data['msg'])
    console.log("you entered ", func_area)
    sio.emit('get_func_area', {"func_area": func_area});
});


sio.on('rsp_func_area', (data) => {
    console.log(data['msg'])
    soln_purpose = window.prompt(data['msg'])
    console.log("you entered ", soln_purpose)
    sio.emit('get_soln_owner_nm', {"soln_purpose": soln_purpose});
});



sio.on('rsp_soln_owner_nm', (data) => {
    console.log(data["msg"])
    sol_owner = window.prompt(data['msg'])
    console.log("you entered ", sol_owner)
    sio.emit('get_soln_user', {"sol_owner": sol_owner});
})


sio.on('rsp_soln_user', (data) => {
    console.log(data["msg"])
    sol_user = window.prompt(data['msg'])
    console.log("you entered ", sol_user)
    sio.emit('get_total_chapter', {"sol_user": sol_user});
})


sio.on('rsp_total_chapter', (data) => {
    console.log(data["msg"])
    total_chapter = window.prompt(data['msg'])
    console.log("you entered ", total_chapter)
    //sio.emit('get_chapters_nm', {"sol_WA": sol_write_access});
    sio.emit('get_chapters_nm', {"total_chapter": total_chapter});
})


sio.on('rsp_loop_cu', (data) => {
    //console.log(data["msg"])
    //sol_write_access = window.prompt(data['msg'])
    loc = "In loop"
    console.log("looping here")
    //sio.emit('get_chapters_nm', {"sol_WA": sol_write_access});
    sio.emit('get_chapters_nm', {"loc": loc});
})


sio.on('rsp_chapters_nm', (data) => {
    console.log(data["msg"])
    chapter_names = window.prompt(data['msg'])
    console.log("you entered ", chapter_names)
    sio.emit('get_chapter_purpose', {"chapter_names": chapter_names});
})


sio.on('rsp_chapter_purpose', (data) => {
    console.log(data["msg"])
    chapter_purpose = window.prompt(data['msg'])
    console.log("you entered ", chapter_purpose)
    sio.emit('get_chapter_ipmethod', {"chapter_purpose": chapter_purpose});
})


sio.on('rsp_chapter_ipmethod', (data) => {
    console.log(data["msg"])
    chapter_ipmethod = window.prompt(data['msg'])
    console.log("you entered ", chapter_ipmethod)
    sio.emit('get_each_owner_dtl', {"chapter_ipmethod": chapter_ipmethod});
})


sio.on('rsp_chapter_owner', (data) => {
    console.log(data["msg"])
    chapter_owner = window.prompt(data['msg'])
    console.log("you entered ", chapter_owner)
    sio.emit('get_each_user_dtl', {"chapter_owner": chapter_owner});
})


sio.on('rsp_chapter_user', (data) => {
    console.log(data["msg"])
    chapter_user = window.prompt(data['msg'])
    console.log("you entered ", chapter_user)
    sio.emit('get_object_count', {"chapter_user": chapter_user});
})


sio.on('rsp_obj_count', (data) => {
    console.log(data["msg"])
    obj_count = window.prompt(data['msg'])
    console.log("you entered ", obj_count)
    sio.emit('get_next_step', {"obj_count": obj_count});
})


sio.on('rsp_each_step_entity', (data) => {

})

/*sio.on('connect_error', (e) => {
    console.log("Connection Error:"+ e)
})*/

sio.on('disconnect',() => {
    console.log("disconnected");
});
