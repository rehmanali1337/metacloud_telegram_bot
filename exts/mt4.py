from metaapi_cloud_sdk import MetaApi, clients
import json
import asyncio
import logging
import config


class MT4:
    def __init__(self):
        self.api = MetaApi(config.METACLOUD_API_KEY)
        self.loginfo = logging.getLogger(' MT4 ').warning
        self.account = None

    async def createProfile(self, profileName: str = None, brokerTimezone: str = None,
                            brokerDSTSwitchTimezone: str = None, serversFile: str = None, version: int = 4):

        provisioningProfile = await self.api.provisioning_profile_api.create_provisioning_profile({
            'name': profileName,
            'version': version,
            'brokerTimezone': brokerTimezone,
            'brokerDSTSwitchTimezone': brokerDSTSwitchTimezone
        })
        await provisioningProfile.upload_file('broker.srv', serversFile)
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
        accounts = await self.api.metatrader_account_api.get_accounts()
        if len(accounts) == 0:
            return False
        return True

    async def get_account(self):
        if self.account is None:
            accounts = await self.api.metatrader_account_api.get_accounts()
            if len(accounts) == 0:
                print('No Accounts added to terminal.')
                return False
            self.account = accounts[0]
            return True

    async def getDeployedAccounts(self, **kwargs):
        accounts = await self.api.metatrader_account_api.get_accounts({
            'limit': 10,
            'offset': 0,
            'state': [kwargs.get('state', 'DEPLOYED')]
        })
        return accounts

    async def createBuyOrder(self, symbol, sl, tp, price):
        volume = config.LOT_VALUE
        status = await self.get_account()
        if not status:
            return
        try:
            connection = await self.account.connect()
            print('Account connected!')
            await connection.wait_synchronized()
            print('Account synched!')
        except clients.timeoutException.TimeoutException:
            self.loginfo('Sync time out..\nTrying again..')
            await connection.close()
            await self.createBuyOrder(symbol, sl, tp, price)
            return
        try:
            self.loginfo(f'Symbol : {symbol}')
            self.loginfo(f'Volume : {volume}')
            self.loginfo(f'TP : {tp}')
            self.loginfo(f'SL : {sl}')
            self.loginfo(f'Open Price : {price}')
            await connection.create_limit_buy_order(symbol=str(symbol),
                                                    volume=float(volume), open_price=float(price),
                                                    stop_loss=float(sl), take_profit=float(tp),
                                                    options={'comment': 'comment', 'clientId': 'TE_GBPUSD_7hyINWqAl'})
            self.loginfo(f'Order Execution successfull!')
            await connection.close()
        except clients.metaApi.tradeException.TradeException as e:
            self.loginfo('Trade execution failed because of trade exception!')
            self.loginfo(e.__dict__)
            return None

    async def createSellOrder(self, symbol, sl, tp, price):
        volume = config.LOT_VALUE
        status = await self.get_account()
        if not status:
            return
        try:
            connection = await self.account.connect()
            print('Account connected!')
            await connection.wait_synchronized()
            print('Account synched!')
        except clients.timeoutException.TimeoutException:
            self.loginfo('Sync time out..\nTrying again..')
            await connection.close()
            await self.createSellOrder(symbol, sl, tp, price)
            return
        try:
            self.loginfo(f'Symbol : {symbol}')
            self.loginfo(f'Volume : {volume}')
            self.loginfo(f'TP : {tp}')
            self.loginfo(f'SL : {sl}')
            self.loginfo(f'Open Price : {price}')
            await connection.create_limit_sell_order(symbol=str(symbol),
                                                     volume=float(volume), stop_loss=float(sl),
                                                     take_profit=float(tp), open_price=float(
                price))
            self.loginfo(f'Order Execution successfull!')
            await connection.close()
            return
        except clients.metaApi.tradeException.TradeException as e:
            self.loginfo('Trade execution failed because of trade exception!')
            self.loginfo(e.__dict__)
            return None

    async def createDemoAccount(self, provisioningProfileID):
        demo_account = await self.api.metatrader_demo_account_api.create_mt4_demo_account(provisioningProfileID, {
            'balance': 100000,
            'email': 'example@example.com',
            'leverage': 100,
            'serverName': 'Exness-Trial4'
        })
        return demo_account


async def main():
    mt = MT4()
    accounts = await mt.getDeployedAccounts()
    accountID = accounts[0].id
    symbol = 'EURUSD'
    volme = 77.00
    stopLoss = 77.70
    take_profit = 76.01
    try:
        res = await mt.createSellOrder(symbol, stopLoss, take_profit, 1)
    except clients.errorHandler.ValidationException as e:
        print(e._details)
    print(res)


if __name__ == "__main__":
    import time
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print("--- %s seconds ---" % (time.time() - start_time))
