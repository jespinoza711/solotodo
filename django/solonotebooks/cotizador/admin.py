from solonotebooks.cotizador.models import *
from django.contrib import admin
from django import forms

admin.site.register(UserProfile)
admin.site.register(AdvertisementPosition)
admin.site.register(Advertisement)
admin.site.register(AdvertisementVisit)
admin.site.register(SearchRegistry)
admin.site.register(ExternalVisit)
admin.site.register(Store)

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
            
class ProductAdmin(admin.ModelAdmin):
    exclude = ['publicized_offer']
    
class NotebookAdmin(admin.ModelAdmin):
    exclude = ['publicized_offer']
    
class VideoCardAdmin(admin.ModelAdmin):
    exclude = ['publicized_offer']
    list_display = ['pretty_display', 'gpu', 'core_clock', 'shader_clock', 'memory_clock']
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(VideoCard, VideoCardAdmin)

class VideoCardGpuAdmin(admin.ModelAdmin):
    list_display = ['pretty_display', 'default_core_clock', 'default_shader_clock', 'default_memory_clock']

admin.site.register(VideoCardGpu, VideoCardGpuAdmin)
