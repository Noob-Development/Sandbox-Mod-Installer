import os
from os.path import join, dirname

from shutil import copyfile, move
import subprocess

import utils.modDownloader

import utils.variables as var


from loggingConfig import setupLogging
logger = setupLogging()


def writeConfig(config_file, new_file, installerConfig):
    try:
        contents = config_file.read()
        splits = contents.split('%')
        for i in range(len(splits)):
            if i % 2:
                try:
                    splits[i] = installerConfig[splits[i]]
                except KeyError:
                    logger.error(f'Key error with {splits[i]}')
        new_file.write(''.join(splits))
    except Exception as e:
        logger.error(f'Failed to write config: {e}')
        raise

def runInstall():
    #Get game variant
    try:
        dir_path = var.installLocation
        base_folder = os.path.basename(os.path.normpath(var.installLocation))
        if base_folder == 'Wargame Red Dragon':
            game_variant = 'Steam'
        elif base_folder == 'WargameRedDragon':
            game_variant = 'Epic'
        else:
            logger.error('Something is wrong, no game variant found????')
            exit()
        logger.info(f'Game variant: {game_variant}')

        #Load installation paths
        logger.info('Getting install config')
        install_config = utils.modDownloader.loadConfiguration()

        #Logging patches applied
        if var.patches_to_apply == []:
            logger.info('No patches applied')
            input("Press enter to continue...")
            exit()
        if var.mod_from_backup:
            var.PATCHES_LOG = open(join(dir_path, var.MOD_FOLDER, var.PATCHES_LOG), 'w+', encoding='utf-8')
        else:
            var.PATCHES_LOG = open(join(dir_path, var.MOD_FOLDER, var.PATCHES_LOG), 'w+', encoding='utf-8')
        for patch in var.patches_to_apply:
            var.PATCHES_LOG.write(patch)
            var.PATCHES_LOG.write('\n')
        var.PATCHES_LOG.close()


        #Make original NDF_Win.dat file if needed
        pc_path = join('Data', 'WARGAME', 'PC')
        ndf_path = join(pc_path, install_config[game_variant]["NDF_Win.dat"], "NDF_Win.dat")
        full_ndf_path = join(dir_path, ndf_path)
        if not os.path.isfile(full_ndf_path+var.PRESANDBOX_SUFFIX):
            logger.warning('Backup does not exist, creating one!')
            copyfile(full_ndf_path, full_ndf_path+var.PRESANDBOX_SUFFIX)
        else:
            if var.mod_from_backup:
                os.remove(full_ndf_path)
                copyfile(full_ndf_path + var.PRESANDBOX_SUFFIX, full_ndf_path)

        #Call patcher
        logger.info('')
        logger.info('This can take up to 10 minutes to complete! The installer will say when its done!')
        logger.info('')

        patcher_call_list = []
        for patch_path in var.patches_to_apply:
            patcher_call_list += [f'{dir_path}\\{var.MOD_FOLDER}\\Script Library\\{patch_path}']
        patcher_call = [f'{dir_path}\\{var.MOD_FOLDER}\\Patcher\\WGPatcher.exe', 'apply', full_ndf_path] + patcher_call_list
        logger.info(f'Patcher Call: {" ".join(patcher_call)}')

        # Run the patcher and log the output
        process = subprocess.Popen(patcher_call, cwd=dir_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        for stdout_line in iter(process.stdout.readline, ""):
            logger.info(stdout_line.strip())
        for stderr_line in iter(process.stderr.readline, ""):
            logger.error(stderr_line.strip())

        process.stdout.close()
        process.stderr.close()
        process.wait()

        move(join(dirname(full_ndf_path), 'ndf_win_patched.dat'), full_ndf_path)

        #Make installerConfig
        logger.debug('Making asset installer config file')
        config_replacements = {
            'mod_version': utils.modDownloader.getCurrentVersion(),
            'game_version': install_config[game_variant]["NDF_Win.dat"],
            'NDF_Win.dat-path': install_config[game_variant]["NDF_Win.dat"],
            'ZZ_Win.dat|interface_outgame-path': install_config[game_variant]["ZZ_Win.dat-interface_outgame"],
            'Data.dat-path': install_config[game_variant]["Data.dat"],
            'ZZ_4.dat-path': install_config[game_variant]["ZZ_4.dat"],}
        with open(join(dir_path, var.MOD_FOLDER, 'Installer', 'installerConfigTemplate.wmi'), encoding='utf-8') as config_file, open(join(dir_path, var.MOD_FOLDER, 'Installer', 'installerConfig.wmi'), 'w+', encoding='utf-8') as new_file:
            logger.debug('Writing to installer config file')
            writeConfig(config_file, new_file, config_replacements)

        #Run asset installer
        logger.info('Running asset installer!')
        asset_installer = subprocess.run('WargameModInstaller.exe', cwd=join(dir_path, var.MOD_FOLDER, 'Installer'), shell=True)

        logger.info('Finished!')


    except Exception as e:
        logger.critical(f'{e}')
        input("Press enter to exit...")
