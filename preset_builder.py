#!/usr/bin/python3
from operator import index
from format_preset import format_preset
import math
import torch


def map_range(x, in_min, in_max, out_min, out_max):
    in_range = in_max - in_min
    in_delta = x - in_min
    if in_range != 0:
        mapped = in_delta / in_range
    elif in_delta != 0:
        mapped = in_delta
    else:
        mapped = 0.5
    mapped *= out_max - out_min
    mapped += out_min
    if out_min <= out_max:
        return max(min(mapped, out_max), out_min)
    return min(max(mapped, out_max), out_min)


def build_preset(data, name):
    mapped_data = []
    print(data)
    mapped_data.append(map_range(data[0].item(), -1, 1, 0, 2.5))

    mapped_data.append(map_range(data[1].item(), -1, 1, 0, 2.5))
    mapped_data.append(map_range(data[2].item(), -1, 1, 0, 1))
    mapped_data.append(map_range(data[3].item(), -1, 1, 0, 2.5))
    mapped_data.append(math.floor(map_range(data[4].item(), -1, 1, 0, 4)))
    mapped_data.append(map_range(data[5].item(), -1, 1, 0, 2.5))
    mapped_data.append(map_range(data[6].item(), -1, 1, 0, 2.5))
    # Filter Sustain
    mapped_data.append(map_range(data[7].item(), -1, 1, 0, 1))
    # Filter Release
    mapped_data.append(map_range(data[8].item(), -1, 1, 0, 2.5))
    mapped_data.append(map_range(data[9].item(), -1, 1, 0, 0.97))  # Resonance
    mapped_data.append(map_range(data[10].item(), -1, 1, -16, 16))  # Amount
    mapped_data.append(map_range(data[11].item(), -1, 1, -0.5, 1.5))
    mapped_data.append(map_range(data[12].item(), -1, 1, -1, 1))  # Detune
    mapped_data.append(math.floor(
        map_range(data[13].item(), -1, 1, 0, 4)))  # OSC 2 waveform
    mapped_data.append(map_range(data[14].item(), -1, 1, 0, 1))
    mapped_data.append(map_range(data[15].item(), -1, 1, 0, 7.5))  # LFO freq
    mapped_data.append(math.floor(
        map_range(data[16].item(), -1, 1, 0, 6)))  # LFO Waveform
    mapped_data.append(map_range(data[17].item(), -1, 1, -3, 4))
    mapped_data.append(map_range(data[18].item(), -1, 1, -1, 1))  # OSC MIX
    mapped_data.append(map_range(data[19].item(), -1, 1, 0, 1.2599))
    mapped_data.append(map_range(data[20].item(), -1, 1, -1, 1))
    # AMP Mod Amount
    mapped_data.append(map_range(data[21].item(), -1, 1, -1, 1))

    for i in range(22, 29):
        mapped_data.append(map_range(data[i].item(), -1, 1, 0, 1))

    # Distortion Crunch
    mapped_data.append(map_range(data[29].item(), -1, 1, 0, 0.9))
    mapped_data.append(math.floor(
        map_range(data[30].item(), -1, 1, 0, 1)))  # Osc 2 Sync
    mapped_data.append(map_range(data[31].item(), -1, 1, 0, 1))  # Port time
    mapped_data.append(map_range(data[32].item(), -1, 1, 0, 2))
    mapped_data.append(math.floor(
        map_range(data[33].item(), -1, 1, -12, 12)))  # Osc Pitch
    mapped_data.append(map_range(data[34].item(), -1, 1, 0, 4))  # Filter Type
    mapped_data.append(map_range(data[35].item(), -1, 1, 0, 1))  # Filter Slope
    mapped_data.append(map_range(data[36].item(), -1, 1, 0, 2))  # Freq Mod Osc

    for i in range(37, 41):
        mapped_data.append(math.floor(map_range(data[i].item(), -1, 1, 0, 1)))

    CSV_HEADER = ['amp_attack', 'amp_decay', 'amp_sustain', 'amp_release', 'osc1_waveform', 'filter_attack', 'filter_decay', 'filter_sustain', 'filter_release', 'filter_resonance', 'filter_env_amount', 'filter_cutoff', 'osc2_detune', 'osc2_waveform', 'master_vol', 'lfo_freq', 'lfo_waveform', 'osc2_range', 'osc_mix', 'freq_mod_amount', 'filter_mod_amount',
                  'amp_mod_amount', 'osc_mix_mode', 'osc1_pulsewidth', 'osc2_pulsewidth', 'reverb_roomsize', 'reverb_damp', 'reverb_wet', 'reverb_width', 'distortion_crunch', 'osc2_sync', 'portamento_time', 'keyboard_mode', 'osc2_pitch', 'filter_type', 'filter_slope', 'freq_mod_osc', 'filter_kbd_track', 'filter_vel_sens', 'amp_vel_sens', 'portamento_mode']

    preset_dict = {'preset_name': "test"}

    for i in range(len(mapped_data)):
        preset_dict[CSV_HEADER[i]] = mapped_data[i]

    format_preset(preset_name=name, preset_dict=preset_dict)


def build_format_preset(data, name):
    data[0] = map_range(data[0], -1, 1, 0, 2.5)
    data[1] = map_range(data[1], -1, 1, 0, 2.5)
    data[2] = map_range(data[2], -1, 1, 0, 1)
    data[3] = map_range(data[3], -1, 1, 0, 2.5)
    data[4] = data[PANDAS_HEADERS.index('osc1_waveform_0'):PANDAS_HEADERS.index(
        'osc1_waveform_4')+1].argmax().item()
    data[5] = map_range(data[5], -1, 1, 0, 2.5)
    data[6] = map_range(data[6], -1, 1, 0, 2.5)
    data[7] = map_range(data[7], -1, 1, 0, 1)  # Filter Sustain
    data[8] = map_range(data[8], -1, 1, 0, 2.5)  # Filter Release
    data[9] = map_range(data[9], -1, 1, 0, 0.97)  # Resonance
    data[10] = map_range(data[10], -1, 1, -16, 16)  # Amount
    data[11] = map_range(data[11], -1, 1, -0.5, 1.5)
    # data[12] = map_range(data[12], -1, 1, -1, 1) # Detune
    data[13] = data[PANDAS_HEADERS.index('osc2_waveform_0'):PANDAS_HEADERS.index(
        'osc2_waveform_4')+1].argmax().item()
    data[14] = 0.67  # map_range(data[14], -1, 1, 0, 1) # Master Volume
    data[15] = map_range(data[15], -1, 1, 0, 7.5)  # LFO freq
    data[16] = data[PANDAS_HEADERS.index('lfo_waveform_0'):PANDAS_HEADERS.index(
        'lfo_waveform_6')+1].argmax().item()  # LFO Waveform
    data[17] = data[PANDAS_HEADERS.index('osc2_range_0'):PANDAS_HEADERS.index(
        'osc2_range_7')+1].argmax().item() - 3
    # data[18] = map_range(data[18], -1, 1, -1, 1) # OSC MIX
    data[19] = map_range(data[19], -1, 1, 0, 1.2599)
    # data[20] = map_range(data[20], -1, 1, -1, 1)
    # data[21] = map_range(data[21], -1, 1, -1, 1)  # AMP Mod Amount

    for i in range(22, 29):
        data[i] = map_range(data[i], -1, 1, 0, 1)

    data[29] = 0  # map_range(data[29], -1, 1, 0, 0.9) # Distortion Crunch
    data[30] = data[PANDAS_HEADERS.index('osc2_sync_0'):PANDAS_HEADERS.index(
        'osc2_sync_1')+1].argmax().item()  # Osc 2 Sync
    data[31] = map_range(data[31], -1, 1, 0, 1)  # Port time
    data[32] = data[PANDAS_HEADERS.index('keyboard_mode_0'):PANDAS_HEADERS.index(
        'keyboard_mode_1')+1].argmax().item()  # Keyboard Mode
    data[33] = data[PANDAS_HEADERS.index('osc2_pitch_0'):PANDAS_HEADERS.index(
        'osc2_pitch_24')+1].argmax().item() - 12  # Osc Pitch
    data[34] = data[PANDAS_HEADERS.index('filter_type_0'):PANDAS_HEADERS.index(
        'filter_type_4')+1].argmax().item()  # Filter Type
    data[35] = data[PANDAS_HEADERS.index('filter_slope_0'):PANDAS_HEADERS.index(
        'filter_slope_1')+1].argmax().item()  # Filter Slope
    data[36] = data[PANDAS_HEADERS.index('freq_mod_osc_0'):PANDAS_HEADERS.index(
        'freq_mod_osc_2')+1].argmax().item()  # Freq Mod Osc

    data[37] = 1  # map_range(data[37], -1, 1, 0, 2) # filter kbd track
    data[38] = 1  # map_range(data[38], -1, 1, 0, 2) # FFilter Velocity Sens
    data[39] = 1  # map_range(data[39], -1, 1, 0, 2) # Amp Velocity
    # math.floor(map_range(data[40], -1, 1, 0, 2)) # Portamento Mode
    data[40] = 1

    CSV_HEADER = ['amp_attack', 'amp_decay', 'amp_sustain', 'amp_release', 'osc1_waveform', 'filter_attack', 'filter_decay', 'filter_sustain', 'filter_release', 'filter_resonance', 'filter_env_amount', 'filter_cutoff', 'osc2_detune', 'osc2_waveform', 'master_vol', 'lfo_freq', 'lfo_waveform', 'osc2_range', 'osc_mix', 'freq_mod_amount', 'filter_mod_amount',
                  'amp_mod_amount', 'osc_mix_mode', 'osc1_pulsewidth', 'osc2_pulsewidth', 'reverb_roomsize', 'reverb_damp', 'reverb_wet', 'reverb_width', 'distortion_crunch', 'osc2_sync', 'portamento_time', 'keyboard_mode', 'osc2_pitch', 'filter_type', 'filter_slope', 'freq_mod_osc', 'filter_kbd_track', 'filter_vel_sens', 'amp_vel_sens', 'portamento_mode']

    preset_dict = {'preset_name': "test"}

    for i in range(41):
        preset_dict[CSV_HEADER[i]] = data[i].item()

    format_preset(preset_name=name, preset_dict=preset_dict)


def build_format_preset01(data, name):
    data[0] = map_range(data[0], 0, 1, 0, 2.5)
    data[1] = map_range(data[1], 0, 1, 0, 2.5)
    data[2] = map_range(data[2], 0, 1, 0, 1)
    data[3] = map_range(data[3], 0, 1, 0, 2.5)
    data[4] = data[PANDAS_HEADERS.index('osc1_waveform_0'):PANDAS_HEADERS.index(
        'osc1_waveform_4')+1].argmax().item()
    data[5] = map_range(data[5], 0, 1, 0, 2.5)
    data[6] = map_range(data[6], 0, 1, 0, 2.5)
    data[7] = map_range(data[7], 0, 1, 0, 1)  # Filter Sustain
    data[8] = map_range(data[8], 0, 1, 0, 2.5)  # Filter Release
    data[9] = map_range(data[9], 0, 1, 0, 0.97)  # Resonance
    data[10] = map_range(data[10], 0, 1, -16, 16)  # Amount
    data[11] = map_range(data[11], 0, 1, -0.5, 1.5)
    # data[12] = map_range(data[12], 0, 1, 0, 1) # Detune
    data[13] = data[PANDAS_HEADERS.index('osc2_waveform_0'):PANDAS_HEADERS.index(
        'osc2_waveform_4')+1].argmax().item()
    data[14] = 0.67  # map_range(data[14], 0, 1, 0, 1) # Master Volume
    data[15] = map_range(data[15], 0, 1, 0, 7.5)  # LFO freq
    # data[16] = data[PANDAS_HEADERS.index('lfo_waveform_0'):PANDAS_HEADERS.index(
    #     'lfo_waveform_6')+1].argmax().item()  # LFO Waveform
    data[16] = 0
    data[17] = data[PANDAS_HEADERS.index('osc2_range_0'):PANDAS_HEADERS.index(
        'osc2_range_7')+1].argmax().item() - 3
    # data[18] = map_range(data[18], 0, 1, 0, 1) # OSC MIX
    data[19] = map_range(data[19], 0, 1, 0, 1.2599)
    # data[20] = map_range(data[20], 0, 1, 0, 1)
    # data[21] = map_range(data[21], 0, 1, 0, 1)  # AMP Mod Amount

    for i in range(22, 29):
        data[i] = map_range(data[i], 0, 1, 0, 1)

    data[29] = 0  # map_range(data[29], 0, 1, 0, 0.9) # Distortion Crunch
    data[30] = data[PANDAS_HEADERS.index('osc2_sync_0'):PANDAS_HEADERS.index(
        'osc2_sync_1')+1].argmax().item()  # Osc 2 Sync
    data[31] = map_range(data[31], 0, 1, 0, 1)  # Port time
    data[32] = data[PANDAS_HEADERS.index('keyboard_mode_0'):PANDAS_HEADERS.index(
        'keyboard_mode_1')+1].argmax().item()  # Keyboard Mode
    data[33] = data[PANDAS_HEADERS.index('osc2_pitch_0'):PANDAS_HEADERS.index(
        'osc2_pitch_24')+1].argmax().item() - 12  # Osc Pitch
    data[34] = data[PANDAS_HEADERS.index('filter_type_0'):PANDAS_HEADERS.index(
        'filter_type_4')+1].argmax().item()  # Filter Type
    data[35] = data[PANDAS_HEADERS.index('filter_slope_0'):PANDAS_HEADERS.index(
        'filter_slope_1')+1].argmax().item()  # Filter Slope
    data[36] = data[PANDAS_HEADERS.index('freq_mod_osc_0'):PANDAS_HEADERS.index(
        'freq_mod_osc_2')+1].argmax().item()  # Freq Mod Osc

    data[37] = 1  # map_range(data[37], 0, 1, 0, 2) # filter kbd track
    data[38] = 1  # map_range(data[38], 0, 1, 0, 2) # FFilter Velocity Sens
    data[39] = 1  # map_range(data[39], 0, 1, 0, 2) # Amp Velocity
    # math.floor(map_range(data[40], 0, 1, 0, 2)) # Portamento Mode
    data[40] = 1

    CSV_HEADER = ['amp_attack', 'amp_decay', 'amp_sustain', 'amp_release', 'osc1_waveform', 'filter_attack', 'filter_decay', 'filter_sustain', 'filter_release', 'filter_resonance', 'filter_env_amount', 'filter_cutoff', 'osc2_detune', 'osc2_waveform', 'master_vol', 'lfo_freq', 'lfo_waveform', 'osc2_range', 'osc_mix', 'freq_mod_amount', 'filter_mod_amount',
                  'amp_mod_amount', 'osc_mix_mode', 'osc1_pulsewidth', 'osc2_pulsewidth', 'reverb_roomsize', 'reverb_damp', 'reverb_wet', 'reverb_width', 'distortion_crunch', 'osc2_sync', 'portamento_time', 'keyboard_mode', 'osc2_pitch', 'filter_type', 'filter_slope', 'freq_mod_osc', 'filter_kbd_track', 'filter_vel_sens', 'amp_vel_sens', 'portamento_mode']

    preset_dict = {'preset_name': "test"}

    for i in range(41):
        preset_dict[CSV_HEADER[i]] = data[i].item()

    format_preset(preset_name=name, preset_dict=preset_dict)


PANDAS_HEADERS = ['amp_attack', 'amp_decay', 'amp_sustain', 'amp_release',
                  'filter_attack', 'filter_decay', 'filter_sustain', 'filter_release',
                  'filter_resonance', 'filter_env_amount', 'filter_cutoff', 'lfo_freq',
                  'osc_mix', 'freq_mod_amount', 'filter_mod_amount', 'amp_mod_amount',
                  'osc_mix_mode', 'osc1_pulsewidth', 'osc2_pulsewidth', 'reverb_roomsize',
                  'reverb_damp', 'reverb_wet', 'reverb_width', 'portamento_time',
                  'osc1_waveform_0', 'osc1_waveform_1', 'osc1_waveform_2',
                  'osc1_waveform_3', 'osc1_waveform_4', 'osc2_waveform_0',
                  'osc2_waveform_1', 'osc2_waveform_2', 'osc2_waveform_3',
                  'osc2_waveform_4', 'osc2_range_0', 'osc2_range_1', 'osc2_range_2',
                  'osc2_range_3', 'osc2_range_4', 'osc2_range_5', 'osc2_range_6',
                  'osc2_range_7', 'osc2_sync_0', 'osc2_sync_1', 'keyboard_mode_0',
                  'keyboard_mode_1', 'keyboard_mode_2', 'osc2_pitch_0', 'osc2_pitch_1',
                  'osc2_pitch_2', 'osc2_pitch_3', 'osc2_pitch_4', 'osc2_pitch_5',
                  'osc2_pitch_6', 'osc2_pitch_7', 'osc2_pitch_8', 'osc2_pitch_9',
                  'osc2_pitch_10', 'osc2_pitch_11', 'osc2_pitch_12', 'osc2_pitch_13',
                  'osc2_pitch_14', 'osc2_pitch_15', 'osc2_pitch_16', 'osc2_pitch_17',
                  'osc2_pitch_18', 'osc2_pitch_19', 'osc2_pitch_20', 'osc2_pitch_21',
                  'osc2_pitch_22', 'osc2_pitch_23', 'osc2_pitch_24', 'filter_type_0',
                  'filter_type_1', 'filter_type_2', 'filter_type_3', 'filter_type_4',
                  'filter_slope_0', 'filter_slope_1', 'freq_mod_osc_0', 'freq_mod_osc_1',
                  'freq_mod_osc_2']
