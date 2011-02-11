from solonotebooks.cotizador.models import *
from django.contrib import admin

admin.site.register(UserProfile)
admin.site.register(AdvertisementPosition)
admin.site.register(Advertisement)
admin.site.register(AdvertisementVisit)
admin.site.register(SearchRegistry)
admin.site.register(ExternalVisit)
admin.site.register(Store)

admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(ProductComment)
admin.site.register(ProductPicture)
admin.site.register(ProductPriceChange)
admin.site.register(StoreHasProduct)
admin.site.register(StoreHasProductEntity)
admin.site.register(StoreProductHistory)
admin.site.register(ProductSubscription)
admin.site.register(LogReviveProduct)
admin.site.register(LogLostProduct)
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

admin.site.register(Notebook)
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

admin.site.register(VideoCardGpuBrand)
admin.site.register(VideoCardGpuFamily)
admin.site.register(VideoCardGpuLine)
admin.site.register(VideoCardGpuArchitecture)
admin.site.register(VideoCardGpuCoreFamily)
admin.site.register(VideoCardGpuCore)
admin.site.register(VideoCardPort)
admin.site.register(VideoCardHasPort)
admin.site.register(VideoCardBusName)
admin.site.register(VideoCardBusLane)
admin.site.register(VideoCardBus)
admin.site.register(VideoCardGpuDirectxVersion)
admin.site.register(VideoCardGpuOpenglVersion)
admin.site.register(VideoCardRefrigeration)
admin.site.register(VideoCardSlotType)
admin.site.register(VideoCardProfile)
admin.site.register(VideoCardMemoryType)
admin.site.register(VideoCardMemoryQuantity)
admin.site.register(VideoCardMemoryBusWidth)
admin.site.register(VideoCardGpuCoreCount)
admin.site.register(VideoCardGpuPowerConnector)
admin.site.register(VideoCardGpuManufacturingProcess)
admin.site.register(VideoCardGpu)
admin.site.register(VideoCard)
