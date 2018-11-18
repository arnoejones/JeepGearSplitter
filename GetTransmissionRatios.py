# Refactored out of the graph programs.
# adding more shit from the Mac version
#adding from the win machine now, dammit
# ok, from mac to win again.  Make changes, commit, but uncheck other files, VCS/
import WranglerRatiosLookup


class GetTransmissionRatios():

    def get_trans_ratios(final_dict):
        gear_ratios = []
        # --- determine which transmission list to use ---
        # --- automatic transmisions ---
        if final_dict['jeep_model'] == 'jk_2012' and final_dict['transmissionType'] == 'auto':
            gear_ratios = WranglerRatiosLookup.jk_2012_auto_trans_ratios()
        if final_dict['jeep_model'] == 'jk_2007' and final_dict['transmissionType'] == 'auto':
            gear_ratios = WranglerRatiosLookup.jk_2007_auto_trans_ratios()
        if final_dict['jeep_model'] == 'jl' and final_dict['transmissionType'] == 'auto':
            gear_ratios = WranglerRatiosLookup.jl_automatic_trans_ratios()

        # --- manual transmissions ---
        if final_dict['jeep_model'] == 'jk_2012' and final_dict['transmissionType'] == 'manual':
            gear_ratios = WranglerRatiosLookup.jk_2012_manual_trans_ratios()
        if final_dict['jeep_model'] == 'jk_2007' and final_dict['transmissionType'] == 'manual':
            gear_ratios = WranglerRatiosLookup.jk_2007_manual_trans_ratios()
        if final_dict['jeep_model'] == 'jl' and final_dict['transmissionType'] == 'manual':
            gear_ratios = WranglerRatiosLookup.jl_manual_trans_ratios()
        return gear_ratios

    def get_tcase_ratios(numbers_dict):
        if numbers_dict['fourLowEngaged'] is True and numbers_dict['rubicon'] is True:
            transfercase_final_value = 4  # rubicon
        elif numbers_dict['fourLowEngaged'] is True and numbers_dict['rubicon'] is False:
            transfercase_final_value = 2.76  # non-rubicon
        else:
            transfercase_final_value = 1  # not engaged, so 1:1
        return transfercase_final_value
