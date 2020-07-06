import bpy

#obj = bpy.context.active_object

#propname = "testName"


def setupProperty(obj, propname):
    
    propExists, driverExists, uvExists, modifierExists, driverIndex = checkName(obj,propname)
    
    name = "CPA_" + propname
    
    if not propExists:
        obj['_RNA_UI'] = {}
        obj[name] = 0.0
        obj['_RNA_UI']["CPA_" + propname] = {"description":name,
                          "default": 0.0,
                          "soft_min":0.0,
                          "soft_max":1.0,
                          "is_overridable_library":0,
                          }
    if not uvExists:
        obj.data.uv_layers.new(name=name)
        
        for loop in obj.data.loops :
            obj.data.uv_layers[name].data[loop.index].uv = (0.0,0.0)

    if not modifierExists:
        
        #If the driver already exists somewhere, remove it.
        if driverExists:
            driver = obj.animation_data.drivers[driverIndex]
            del driver
            print("Property Setup: Driver found and deleted")
        else:
            print("Property Setup: No driver found, all okay")
        
        warpmod = obj.modifiers.new(name=name, type='UV_WARP')
        warpmod.show_expanded = False
        obj.modifiers[name].driver_remove('offset',0)
        warpmod.uv_layer = name
        
        driverIndex = createDriver(obj, propname)
        
        driverExists = True
    
    #Modifier exists, driver doesn't
    if not driverExists and modifierExists:
        
        obj.modifiers[name].uv_layer = name
        
        driverIndex = createDriver(obj, propname)
    
    
    updateDriverDependencies(obj.animation_data.drivers[driverIndex].driver)    
        
    return {'FINISHED'}

def removeProperty(obj, propname):
    
    propExists, driverExists, uvExists, modifierExists, driverIndex = checkName(obj,propname)
    
    name = "CPA_" + propname
    
    if propExists:
        del obj[name]
        print(str(obj) + " deleted Prop")
    
    if driverExists:
        driver = obj.animation_data.drivers[driverIndex]
        del driver
        print("Property Remove: Found Driver and deleted it")
        print(str(obj) + " deleted Driver")
    
    if driverExists and modifierExists:
        obj.modifiers[name].driver_remove('offset',0)
        print(str(obj) + " deleted Driver in Modifier")
    
    if modifierExists:
        obj.modifiers.remove(obj.modifiers.get(name))
        print(str(obj) + " deleted Modifier")

    if uvExists:
        #obj.data.uv_layers[name].active = True
        #bpy.ops.mesh.uv_texture_remove()
        
        obj.data.uv_layers.remove(obj.data.uv_layers.get(name))
        
        print(str(obj) + " deleted UV")
    
    return {'FINISHED'}

def checkName(obj, propname):
    name = "CPA_" + propname
    
    propExists = False
    driverExists = False
    uvExists = False
    modifierExists = False
    driverIndex = 0
    
    try:
        if obj[name] != None:
            propExists = True
        print("Checker: prop found")
    except:
        print("Checker: prop not found")
    
    try:
        if len(obj.animation_data.drivers) == 0:
            raise Exception("No drivers")
            
        for num, driver in enumerate(obj.animation_data.drivers):
            if driver.driver.expression == name:
                driverExists = True
                driverIndex = num
                print("Checker: driver found")
    except:
        print("Checker: driver not found")
    
    try:
        if obj.data.uv_layers[name] != None:
            uvExists = True
        print("Checker: uv found")
    except:
        print("Checker: uv not found")
    
    try:
        if obj.modifiers[name] != None:
            modifierExists = True
        print("Checker: modifier found")
    except:
        print("Checker: modifier not found")
        
    return propExists, driverExists, uvExists, modifierExists, driverIndex

def createDriver(obj, propname):
    name = "CPA_" + propname
    
    obj.modifiers[name].driver_add('offset', 0)
    
    driver = obj.animation_data.drivers[-1].driver

    driver.variables.new()
    curdri = driver.variables[0]
    curdri.name = name
    curdri.type = 'SINGLE_PROP'
    curdri.targets[0].id = obj
    curdri.targets[0].data_path = "[\"" + name + "\"]"
    driver.expression = name
    
    return len(obj.animation_data.drivers) - 1

def updateDriverDependencies(driver):
    driver.expression += " "
    driver.expression = driver.expression[:-1]


#print("------------------")
#setupProperty(obj, propname)
#removeProperty(obj, propname)