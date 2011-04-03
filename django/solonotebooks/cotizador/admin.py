from solonotebooks.cotizador.models import *
from django.contrib import admin
from django import forms

admin.site.register(UserProfile)
admin.site.register(AdvertisementPosition)
admin.site.register(Advertisement)
admin.site.register(AdvertisementVisit)
admin.site.register(SearchRegistry)
admin.site.register(ExternalVisit)
admin.site.register(SponsoredVisit)
admin.site.register(Store)

admin.site.register(InterfaceBrand)
admin.site.register(InterfaceVideoPort)
admin.site.register(InterfaceCardBus)
admin.site.register(InterfaceSocketBrand)
admin.site.register(InterfaceSocket)
admin.site.register(InterfacePowerConnector)
admin.site.register(InterfacePort)
admin.site.register(InterfaceMemoryType)
admin.site.register(InterfaceBus)

admin.site.register(ProductType)
admin.site.register(ProductComment)
admin.site.register(ProductPicture)
admin.site.register(ProductPriceChange)
admin.site.register(StoreHasProduct)
admin.site.register(StoreHasProductEntity)
admin.site.register(StoreProductHistory)
admin.site.register(ProductSubscription)
admin.site.register(LogFetchStoreError)
admin.site.register(LogReviveProduct)
admin.site.register(LogLostProduct)
admin.site.register(LogChangeEntityName)
admin.site.register(LogChangeProductPrice)
admin.site.register(MailChangeProductPrice)
admin.site.register(MailLostProduct)
admin.site.register(MailReviveProduct)
admin.site.register(ProductComparisonList)
admin.site.register(ProductVisit)

admin.site.register(LogNewEntity)
admin.site.register(LogReviveEntity)
admin.site.register(LogLostEntity)
admin.site.register(LogChangeEntityPrice)

admin.site.register(LogEntry)
admin.site.register(LogEntryMessage)

admin.site.register(NotebookLine)
admin.site.register(NotebookBrand)
admin.site.register(NotebookCardReader)
admin.site.register(NotebookType)
admin.site.register(NotebookChipsetBrand)
admin.site.register(NotebookChipset)
admin.site.register(NotebookLan)
admin.site.register(NotebookOpticalDrive)
admin.site.register(NotebookOperatingSystemBrand)
admin.site.register(NotebookOperatingSystemFamily)
admin.site.register(NotebookOperatingSystemLanguage)
admin.site.register(NotebookOperatingSystem)
admin.site.register(NotebookPowerAdapter)
admin.site.register(NotebookProcessorBrand)
admin.site.register(NotebookProcessorLine)
admin.site.register(NotebookProcessorLineFamily)
admin.site.register(NotebookProcessorFrequency)
admin.site.register(NotebookProcessorCache)
admin.site.register(NotebookProcessorFSB)
admin.site.register(NotebookProcessorMultiplier)
admin.site.register(NotebookProcessorSocket)
admin.site.register(NotebookProcessor)
admin.site.register(NotebookProcessorFamily)
admin.site.register(NotebookProcessorManufacturing)
admin.site.register(NotebookRamQuantity)
admin.site.register(NotebookRamType)
admin.site.register(NotebookRamFrequency)
admin.site.register(NotebookScreenResolution)
admin.site.register(NotebookScreenSizeFamily)
admin.site.register(NotebookScreenSize)
admin.site.register(NotebookScreen)
admin.site.register(NotebookVideoCardMemory)
admin.site.register(NotebookVideoCardType)
admin.site.register(NotebookVideoCardLine)
admin.site.register(NotebookVideoCardBrand)
admin.site.register(NotebookVideoCard)
admin.site.register(NotebookStorageDriveType)
admin.site.register(NotebookStorageDriveRpm)
admin.site.register(NotebookStorageDriveCapacity)
admin.site.register(NotebookStorageDrive)
admin.site.register(NotebookWifiCardBrand)
admin.site.register(NotebookWifiCardNorm)
admin.site.register(NotebookWifiCard)
admin.site.register(NotebookVideoPort)

admin.site.register(VideoCardBrand)
admin.site.register(VideoCardGpuBrand)
admin.site.register(VideoCardGpuFamily)
admin.site.register(VideoCardGpuLine)
admin.site.register(VideoCardGpuArchitecture)
admin.site.register(VideoCardGpuCoreFamily)
admin.site.register(VideoCardGpuCore)
admin.site.register(VideoCardPort)
admin.site.register(VideoCardHasPort)
admin.site.register(InterfaceCardBusName)
admin.site.register(InterfaceCardBusLane)
admin.site.register(VideoCardBus)
admin.site.register(VideoCardGpuDirectxVersion)
admin.site.register(VideoCardGpuOpenglVersion)
admin.site.register(VideoCardRefrigeration)
admin.site.register(VideoCardSlotType)
admin.site.register(VideoCardProfile)
admin.site.register(VideoCardPowerConnector)
admin.site.register(VideoCardHasPowerConnector)
admin.site.register(VideoCardMemoryType)
admin.site.register(VideoCardMemoryQuantity)
admin.site.register(VideoCardMemoryBusWidth)
admin.site.register(VideoCardGpuCoreCount)
admin.site.register(VideoCardGpuManufacturingProcess)

excludes = ['ptype', 'shp', 'week_visitor_count', 'week_discount', 'long_description', 'similar_products', 'sponsored_shp']
            
class ProductAdmin(admin.ModelAdmin):
    exclude = excludes
    
class VideoCardAdmin(admin.ModelAdmin):
    exclude = excludes
    list_display = ['pretty_display', 'core_clock', 'shader_clock', 'memory_clock']
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Notebook, ProductAdmin)
admin.site.register(VideoCard, VideoCardAdmin)

class VideoCardGpuAdmin(admin.ModelAdmin):
    list_display = ['pretty_display', 'default_core_clock', 'default_shader_clock', 'default_memory_clock']

admin.site.register(VideoCardGpu, VideoCardGpuAdmin)


admin.site.register(ProcessorBrand)
admin.site.register(ProcessorFamily)
admin.site.register(ProcessorLine)
admin.site.register(ProcessorL2CacheQuantity)
admin.site.register(ProcessorL3CacheQuantity)
admin.site.register(ProcessorL2Cache)
admin.site.register(ProcessorL3Cache)
admin.site.register(ProcessorSocket)
admin.site.register(ProcessorCoreCount)
admin.site.register(ProcessorArchitecture)
admin.site.register(ProcessorManufacturingProcess)
admin.site.register(ProcessorCore)
admin.site.register(ProcessorMultiplier)
admin.site.register(ProcessorFsb)
admin.site.register(ProcessorGraphics)

class ProcessorAdmin(admin.ModelAdmin):
    exclude = excludes
    list_display = ['pretty_display', 'pcmark_id', 'pcmark_05_score', 'pcmark_vantage_score', 'passmark_score']

admin.site.register(Processor, ProcessorAdmin)

admin.site.register(ScreenType)
admin.site.register(ScreenBrand)
admin.site.register(ScreenLine)
admin.site.register(ScreenDisplayType)
admin.site.register(ScreenDisplay)
admin.site.register(ScreenSizeFamily)
admin.site.register(ScreenSize)
admin.site.register(ScreenAspectRatio)
admin.site.register(ScreenResolution)
admin.site.register(ScreenVideoPort)
admin.site.register(ScreenHasVideoPort)
admin.site.register(ScreenPanelType)
admin.site.register(ScreenSpeakers)
admin.site.register(ScreenResponseTime)
admin.site.register(ScreenRefreshRate)
admin.site.register(ScreenDigitalTuner)
admin.site.register(Screen, ProductAdmin)

admin.site.register(MotherboardBrand)
admin.site.register(MotherboardGraphics)
admin.site.register(MotherboardSocket)
admin.site.register(MotherboardSouthbridge)
admin.site.register(MotherboardChipsetBrand)
admin.site.register(MotherboardNorthbridgeFamily)
admin.site.register(MotherboardNorthbridge)
admin.site.register(MotherboardChipset)
admin.site.register(MotherboardPort)
admin.site.register(MotherboardHasPort)
admin.site.register(MotherboardFormat)
admin.site.register(MotherboardMemoryType)
admin.site.register(MotherboardHasMemoryType)
admin.site.register(MotherboardCardBus)
admin.site.register(MotherboardHasCardBus)
admin.site.register(MotherboardBus)
admin.site.register(MotherboardHasBus)
admin.site.register(MotherboardVideoPort)
admin.site.register(MotherboardHasVideoPort)
admin.site.register(MotherboardPowerConnector)
admin.site.register(MotherboardHasPowerConnector)
admin.site.register(MotherboardMemoryChannel)
admin.site.register(MotherboardAudioChannels)
admin.site.register(Motherboard, ProductAdmin)

admin.site.register(CellCompany)
admin.site.register(CellPricingPlan)
admin.site.register(CellPricing)
admin.site.register(CellPricingTier)
admin.site.register(CellphoneFormFactor)
admin.site.register(CellphoneCategory)
admin.site.register(CellphoneGraphics)
admin.site.register(CellphoneRam)
admin.site.register(CellphoneManufacturer)
admin.site.register(CellphoneOperatingSystem)
admin.site.register(CellphoneKeyboard)
admin.site.register(CellphoneCamera)
admin.site.register(CellphoneCardReader)
admin.site.register(CellphoneScreenSize)
admin.site.register(CellphoneScreenResolution)
admin.site.register(CellphoneScreenColors)
admin.site.register(CellphoneScreen)
admin.site.register(CellphoneProcessor)
admin.site.register(Cellphone)
admin.site.register(Cell, ProductAdmin)
