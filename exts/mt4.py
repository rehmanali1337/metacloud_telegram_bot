from metaapi_cloud_sdk import MetaApi, clients
import json
import asyncio
import logging
import config


class MT4:
    def __init__(self):
        self.loginfo = logging.getLogger(' MT4 ').warning
        self.account = None
        self.connection = None
        self.api = False
        self.mt5_filename = 'servers.dat'
        self.mt_version = 5
        self.init_complete = False

    async def async_init(self):
        if self.init_complete:
            return
        if not self.api:
            self.api = MetaApi(token=config.METACLOUD_ACCOUNT_TOKEN)
        await self.get_account_connection()
        self.init_complete = True

    async def createProfile(self, profileName: str = None, brokerTimezone: str = None,
                            brokerDSTSwitchTimezone: str = None, serversFile: str = None, version: int = 5):

        provisioningProfile = await self.api.provisioning_profile_api.create_provisioning_profile({
            'name': profileName,
            'version': version,
            'brokerTimezone': brokerTimezone,
            'brokerDSTSwitchTimezone': brokerDSTSwitchTimezone
        })
        await provisioningProfile.upload_file(self.mt5_filename, serversFile)
        return provisioningProfile

    async def getAllProfiles(self):
        provisioningProfiles = await self.api.provisioning_profile_api.get_provisioning_profiles()
        return provisioningProfiles

    async def getProfileByID(self, profileID):
        provisioningProfile = await self.api.provisioning_profile_api.get_provisioning_profile(profileID)
        return provisioningProfile

    async def getProfileByName(self, profileName):
        allProfiles = await self.getAllProfiles()
        for profile in allProfiles:
            if profile.name == profileName:
                return profile
        return None

    async def createMT4Account(self, accountName: str = None, accountType: str = 'cloud', accountLogin: str = None,
                               accountPassword: str = None, serverName: str = None, profileID: str = None,
                               application: str = 'MetaApi', magic: int = 1, quoteStreamingIntervalSeconds: float = 0.0):

        try:
            createdAccount = await self.api.metatrader_account_api.create_account({
                'name': accountName,
                'type': 'cloud',
                'login': accountLogin,
                # password can be investor password for read-only access
                'password': accountPassword,
                'server': serverName,
                'provisioningProfileId': profileID,
                'application': application,
                'magic': 1,
                # set to 0 to receive quote per tick
                'quoteStreamingIntervalInSeconds': quoteStreamingIntervalSeconds
            })
        except clients.errorHandler.ValidationException:
            return False, None
        return True, createdAccount

    async def account_exists(self):
        try:
            await self.api.metatrader_account_api.get_account(config.METACLOUD_ACCOUNT_ID)
            return True
        except clients.errorHandler.UnauthorizedException:
            return False

    async def get_account_connection(self):
        if self.connection is None:
            if self.account is None:
                self.account = await self.api.metatrader_account_api.get_account(config.METACLOUD_ACCOUNT_ID)
                initial_state = self.account.state
                deployed_states = ['DEPLOYING', 'DEPLOYED']

                if initial_state not in deployed_states:
                    #  wait until account is deployed and connected to broker
                    print('Deploying account')
                    await self.account.deploy()

                print(
                    'Waiting for API server to connect to broker (may take couple of minutes)')
                await self.account.wait_connected()

            # connect to MetaApi API
            self.connection = await self.account.connect()

            # wait until terminal state synchronized to the local state
            print(
                'Waiting for SDK to synchronize to terminal state (may take some time depending on your history size)')
            await self.connection.wait_synchronized()

    async def getDeployedAccounts(self, **kwargs):
        accounts = await self.api.metatrader_account_api.get_accounts({
            'limit': 10,
            'offset': 0,
            'state': [kwargs.get('state', 'DEPLOYED')]
        })
        return accounts

    async def create_buy_order(self, symbol=None,
                               open_price=None, stop_loss=None,
                               take_profit=None):
        volume = config.LOT_VALUE
        if self.connection is None:
            await self.get_account_connection()
        try:
            info = await self.connection.get_symbol_price(symbol)
            open_price = float(info['ask'])
            self.loginfo(f'Symbol : {symbol}')
            self.loginfo(f'Volume : {volume}')
            self.loginfo(f'TP : {take_profit}')
            self.loginfo(f'SL : {stop_loss}')
            self.loginfo(f'Open Price : {open_price}')
            await self.connection.create_stop_buy_order(
                str(symbol), float(volume), float(open_price),
                float(stop_loss), float(take_profit))
            self.loginfo(f'Order Execution successfull!')
            # await self.connection.close()
            return
        except clients.metaApi.tradeException.TradeException as e:
            self.loginfo('Trade execution failed because of trade exception!')
            self.loginfo(e.__dict__)
            return None

    async def create_sell_order(self, symbol=None,
                                open_price=None, stop_loss=None,
                                take_profit=None):
        volume = config.LOT_VALUE
        if self.connection is None:
            await self.get_account_connection()
        try:
            info = await self.connection.get_symbol_price(symbol)
            open_price = float(info['bid'])
            self.loginfo(f'Symbol : {symbol}')
            self.loginfo(f'Volume : {volume}')
            self.loginfo(f'TP : {take_profit}')
            self.loginfo(f'SL : {stop_loss}')
            self.loginfo(f'Open Price : {open_price}')

            await self.connection.create_stop_sell_order(
                str(symbol), float(volume), float(open_price), float(stop_loss), float(take_profit), options={})
            self.loginfo(f'Order Execution successfull!')
            # await self.connection.close()
            return
        except clients.metaApi.tradeException.TradeException as e:
            self.loginfo('Trade execution failed because of trade exception!')
            self.loginfo(e.__dict__)
            return None
