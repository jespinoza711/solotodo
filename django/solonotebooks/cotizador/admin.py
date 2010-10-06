from solonotebooks.cotizador.models import *
from django.contrib import admin

class StoreHasNotebookAdmin(admin.ModelAdmin):
    list_display = ('custom_name','notebook', 'is_available', 'visitorCount')
    search_fields = ['custom_name']

admin.site.register(ProcessorBrand)
admin.site.register(ProcessorLine)
admin.site.register(ProcessorLineFamily)
admin.site.register(ProcessorFrequency)
admin.site.register(ProcessorCache)
admin.site.register(ProcessorFSB)
admin.site.register(ProcessorMultiplier)
admin.site.register(ProcessorSocket)
admin.site.register(Processor)
admin.site.register(Lan)
admin.site.register(OpticalDrive)
admin.site.register(NotebookBrand)
admin.site.register(NotebookLine)
admin.site.register(OperatingSystemBrand)
admin.site.register(OperatingSystemFamily)
admin.site.register(OperatingSystemLanguage)
admin.site.register(OperatingSystem)
admin.site.register(VideoCardMemory)
admin.site.register(VideoCardType)
admin.site.register(VideoCardLine)
admin.site.register(VideoCardBrand)
admin.site.register(VideoCard)
admin.site.register(WifiCardBrand)
admin.site.register(WifiCardNorm)
admin.site.register(WifiCard)
admin.site.register(VideoPort)
admin.site.register(ScreenResolution)
admin.site.register(ScreenSizeFamily)
admin.site.register(ScreenSize)
admin.site.register(Screen)
admin.site.register(PowerAdapter)
admin.site.register(StorageDriveType)
admin.site.register(StorageDriveRpm)
admin.site.register(StorageDriveCapacity)
admin.site.register(StorageDrive)
admin.site.register(ChipsetBrand)
admin.site.register(Chipset)
admin.site.register(RamQuantity)
admin.site.register(RamType)
admin.site.register(RamFrequency)
admin.site.register(Notebook)
admin.site.register(NotebookReview)
admin.site.register(NotebookComment)
admin.site.register(NotebookPicture)
admin.site.register(NotebookPriceChange)
admin.site.register(City)
admin.site.register(Store)
admin.site.register(Sucursal)
admin.site.register(StoreHasNotebook, StoreHasNotebookAdmin)
admin.site.register(StoreNotebookHistory)
admin.site.register(LogEntry)
admin.site.register(LogEntryMessage)
admin.site.register(ProcessorFamily)
admin.site.register(ProcessorManufacturing)
admin.site.register(NotebookCardReader)
admin.site.register(ExternalVisit)
admin.site.register(AdvertisementPosition)
admin.site.register(Advertisement)
admin.site.register(AdvertisementVisit)
admin.site.register(SearchRegistry)
admin.site.register(NotebookSubscription)
admin.site.register(UserProfile)
admin.site.register(LogNewModel)
admin.site.register(LogReviveModel)
admin.site.register(LogLostModel)
admin.site.register(LogChangeModelPrice)
admin.site.register(LogReviveNotebook)
admin.site.register(LogLostNotebook)
admin.site.register(LogChangeNotebookPrice)
admin.site.register(MailChangeNotebookPrice)
admin.site.register(MailLostNotebook)
