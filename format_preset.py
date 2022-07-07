def format_preset(preset_name="preset", preset_dict={}):
    f = open("./generated_presets/" + preset_name + ".amSynthPreset", "w")
    f.write("amSynth1.0preset\n")
    
    for i in preset_dict:
        if i == "preset_name":
            f.write("<preset> <name> {}\n".format(preset_name))
        else:
            f.write("<parameter> {} {}\n".format(i, preset_dict[i]))
    print("Preset ", preset_name+".amSynthPreset", " successfully generated!")
        
        
        
# format_preset("test", {"preset_name":"This is awesome", "p1":4, "p2":5})