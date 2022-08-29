
import socketio
#import eventlet
import uvicorn
from num2words import num2words

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio,static_files={'/diabetes/track':'./track/'})


cu_counter = 0
cu_first = True
cu_name = []
cu_purpose = []
cu_owner = []
cu_user = []
cu_ipmethod = ""

@sio.event
async def connect(sid, environ):
    
    username= environ.get('HTTP_X_USERNAME')
    print(sid, "connected")


    async with sio.session(sid) as session:
        session['username'] = username
        # session['solutionName'] = null
        # session['soln_Owner']= []
        # session['soln_RA']= []
        # session['soln_WA']= []
        # session['soln_chapters_cnt'] = null
        # session['soln_chapters'] =[]
    print(session)
    

@sio.event
async def disconnect(sid):
    print(sid, "disconnected")

@sio.event
async def greet(sid, data):
    async with sio.session(sid) as session:
        user_nm = session['username']
    msg = "Hello {}, what do you want to build today".format(user_nm)
    await sio.emit('rsp_greet', {'msg':msg}, to=sid)
    #return {'msg' : msg}


@sio.event
async def get_soln_nm(sid, data):
    print(data)
    async with sio.session(sid) as session:
        session["soln_name"] = data["soln_name"]
    msg = "Good, let me assist you in that. \n Please select the Industry category for {} \n 1. AGRICULTURE, ANIMAL HUSBANDRY & FORESTRY \n 2. MANUFACTURING \n 3. CONSTRUCTION \n 4. REAL ESTATE AND RENTING SERVICES \n 5. FINANCIAL INTERMEDIATION SERVICES \n 6. RESEARCH AND DEVELOPMENT \n 7. SERVICES:".format(session["soln_name"])
    print(msg)
    await sio.emit('rsp_soln_name', {'msg':msg}, to=sid)
    #return {'msg' : msg}


@sio.event
async def get_ind_cat(sid, data):
    print(data)
    async with sio.session(sid) as session:
        session["ind_cat"] = data["ind_cat"]
    msg = "Please select the functional area for {} : \n 1.Production \n 2.Research and Development \n 3. Purchase and Supply \n 4. Marketing \n 5. Human Resource \n 6. Finance and Accounting \n 7. Administration".format(session["soln_name"])
    print(msg)
    await sio.emit('rsp_industry_cat', {'msg':msg}, to=sid)
    #return {'msg' : msg}
    

@sio.event
async def get_func_area(sid, data):
    print(data)
    async with sio.session(sid) as session:
        session["func_area"] = data["func_area"]
    msg = "What is the purpose of {}".format(session["soln_name"])
    print(msg)
    await sio.emit('rsp_func_area', {'msg':msg}, to=sid)
    #return {'msg' : msg}


@sio.event
async def get_soln_owner_nm(sid, data):
    print(data)
    async with sio.session(sid) as session:
        session["soln_purpose"] = data["soln_purpose"]
    msg ="Who is the owner of the solution - {}".format(session["soln_name"])
    print(msg)
    await sio.emit('rsp_soln_owner_nm', {'msg':msg}, to=sid)

@sio.event
async def get_soln_user(sid, data):
    print(data)
    async with sio.session(sid) as session:
       session["soln_owner"]= data["sol_owner"]
    msg ="Who are the users of the solution - {}".format(session["soln_name"])
    print(msg)
    await sio.emit('rsp_soln_user', {'msg':msg}, to=sid)

@sio.event
async def get_total_chapter(sid, data):
    print(data)
    async with sio.session(sid) as session:
       session["sol_user"]= data["sol_user"]
    msg= "How many chapters are there in the solution ? "
    print(msg)
    #await sio.emit('rsp_soln_write_access', {'msg':msg}, to=sid)
    await sio.emit('rsp_total_chapter', {'msg':msg}, to=sid)


@sio.event
#async def get_chapters_nm(sid, data):
async def get_chapters_nm(sid, data):
    #print(data)
    global cu_counter, cu_first
    cu_counter += 1
    if cu_first==True:
        async with sio.session(sid) as session:
            session["total_chapter"]= data["total_chapter"]
            cu_first=False
    chp_count = num2words(cu_counter, to='ordinal')
    msg= "What is the name of the {} chapter ?".format(chp_count)
    await sio.emit('rsp_chapters_nm', {'msg':msg}, to=sid)


@sio.event
async def get_chapter_purpose(sid, data):
    global cu_name
    async with sio.session(sid) as session:
       session["chapter_names"]= data["chapter_names"]
    print(data)
    cu_name.append(session["chapter_names"])
    msg= "What is the purpose of the '{}' chapter ?".format(session["chapter_names"])
    print(msg)
    await sio.emit('rsp_chapter_purpose', {'msg':msg}, to=sid)


@sio.event
async def get_chapter_ipmethod(sid, data):
    global cu_purpose
    async with sio.session(sid) as session:
       session["chapter_purpose"]= data["chapter_purpose"]
    print(data)
    cu_purpose.append(session["chapter_purpose"])
    msg= "Choose input method : \n1.Manual \n2.Automatic ?"
    print(msg)
    await sio.emit('rsp_chapter_ipmethod', {'msg':msg}, to=sid)


@sio.event
async def get_each_owner_dtl(sid, data):
    global cu_name, cu_counter, cu_ipmethod, cu_owner, cu_user
    async with sio.session(sid) as session:
       session["chapter_ipmethod"]= data["chapter_ipmethod"]
    print(data)
    cu_ipmethod = session["chapter_ipmethod"]
    if cu_ipmethod=="Manual":
        msg= "Who is the owner of '{}' ?".format(cu_name[cu_counter-1])
        print(msg)
        await sio.emit('rsp_chapter_owner', {'msg':msg}, to=sid)
    else:
        cu_owner.append(session["soln_owner"])
        cu_user.append(session["sol_user"])
        msg= "How many objects does '{}' contain ?".format(cu_name[cu_counter-1])
        await sio.emit('rsp_obj_count', {'msg':msg}, to=sid)

@sio.event
async def get_each_user_dtl(sid, data):
    global cu_name, cu_counter, cu_ipmethod, cu_user
    async with sio.session(sid) as session:
       session["chapter_owner"]= data["chapter_owner"]
    cu_owner.append(session["chapter_owner"])
    print(data)
    msg= "Who is the user of '{}' ?".format(cu_name[cu_counter-1])
    print(msg)
    #await sio.emit('rsp_chapter_user', {'msg':msg,'options':[]}, to=sid)
    await sio.emit('rsp_chapter_user', {'msg':msg}, to=sid)


@sio.event
async def get_object_count(sid, data):
    global cu_name, cu_counter, cu_user
    async with sio.session(sid) as session:
       session["chapter_user"]= data["chapter_user"]
    cu_user.append(session["chapter_user"])
    print(data)
    msg= "How many objects does '{}' contain ?".format(cu_name[cu_counter-1])
    print(msg)
    await sio.emit('rsp_obj_count', {'msg':msg}, to=sid)


@sio.event
async def get_next_step(sid, data):
    global cu_name, cu_counter, cu_user
    async with sio.session(sid) as session:
       session["obj_count"]= data["obj_count"]
    print(data)
    if cu_counter==int(session["total_chapter"]):
        print("CU_Names: ",cu_name)
        print("CU_Purpose: ",cu_purpose)
        print("CU_Owner: ",cu_owner)
        print("CU_Owner: ",cu_user)
        await sio.emit('disconnect', to=sid)
    else: 
        await sio.emit('rsp_loop_cu', to=sid)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8005)


       