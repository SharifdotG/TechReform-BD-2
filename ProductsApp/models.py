"""Django models for a computer hardware e-commerce application.
This module defines Django ORM models for managing computer hardware products
and accessories. It includes a base abstract model with common fields and
specific models for different product categories.
The models are organized into two main categories:
1. Core Components: CPU, Cooler, Motherboard, RAM, SSD, HDD, GPU, Power Supply, Casing
2. Accessories: Monitor, Keyboard, Mouse, Headphone
Classes:
    BaseProduct: Abstract base model with common product attributes
    CPU: Central Processing Unit model with technical specifications
    Cooler: CPU cooling solution model (air/liquid coolers)
    Motherboard: Motherboard model with socket and connectivity details
    RAM: Memory module model with capacity and speed specifications
    SSD: Solid State Drive model with storage and performance specs
    HDD: Hard Disk Drive model with capacity and mechanical specs
    GPU: Graphics Processing Unit model with memory and performance details
    PowerSupply: Power Supply Unit model with wattage and efficiency ratings
    Casing: Computer case model with form factor and feature details
    Monitor: Display device model with resolution and connectivity options
    Keyboard: Input device model with switch types and layout options
    Mouse: Pointing device model with DPI and button specifications
    Headphone: Audio device model with sound quality and feature details
Each model includes:
- Image fields for product photos (up to 5 images)
- Technical specifications relevant to the product type
- Pricing and inventory management fields
- Category-specific choices for standardized data entry
- Custom save methods to automatically set category
- String representations for admin interface
- Validation using Django validators where appropriate
The BaseProduct abstract model provides common functionality:
- UUID primary key for unique identification
- Pricing fields with discount calculations
- Inventory management (stock, availability)
- Product categorization and metadata
- Timestamps for creation and updates
- Feature flags (featured, new arrival, on sale)
- Property methods for discount calculations and stock status
All models inherit from BaseProduct and extend it with category-specific
fields and choices. The models use Django's ImageField for product images
and include comprehensive help_text for admin interface usability.
Example:
    # Create a new CPU product
    cpu = CPU.objects.create(
        name="Intel Core i7-12700K",
        brand="Intel",
        model="Core i7-12700K",
        price=350.00,
        socket="LGA 1700",
        cores=12,
        threads=20,
        boost_frequency=5.0
    # Check if product is in stock
    if cpu.in_stock:
        print(f"Available: {cpu.stock} units")
    # Calculate discount percentage
    if cpu.discount_percentage > 0:
        print(f"On sale: {cpu.discount_percentage}% off")
Note:
    This module requires Django's ImageField to have Pillow installed
    for image handling. All choice fields use tuples for Django admin
    compatibility and data consistency.
"""

from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator


# Base model for shared attributes
class BaseProduct(models.Model):
    """
    Abstract base model for product entities in the e-commerce system.
    This model provides a common structure for all product types with essential
    fields like pricing, inventory, categorization, and metadata. It serves as
    a foundation for specific product models and includes computed properties
    for discount calculations and stock availability.
    Attributes:
        id (UUIDField): Unique identifier using UUID4, auto-generated and non-editable.
        name (CharField): Product name, up to 200 characters, optional.
        price (DecimalField): Current selling price in BDT, up to 10 digits with 2 decimal places.
        regular_price (DecimalField): Original/regular price in BDT for discount calculations.
        brand (CharField): Brand name, up to 50 characters, optional.
        model (CharField): Product model name, up to 100 characters, optional.
        warranty (CharField): Warranty duration with predefined choices (1-10 years, lifetime).
        description (TextField): Detailed product description, optional.
        category (CharField): Product category from predefined tech hardware categories.
        tdp (IntegerField): Thermal Design Power in watts, primarily for hardware components.
        created_at (DateTimeField): Timestamp when the product was created, auto-set.
        updated_at (DateTimeField): Timestamp when the product was last modified, auto-updated.
        is_featured (BooleanField): Flag indicating if product is featured, defaults to False.
        is_new_arrival (BooleanField): Flag indicating if product is a new arrival, defaults to False.
        is_on_sale (BooleanField): Flag indicating if product is on sale, defaults to False.
        stock (PositiveIntegerField): Available stock quantity, defaults to 0.
        is_available (BooleanField): Product availability status, defaults to True.
    Properties:
        discount_percentage (float): Calculated discount percentage based on regular_price and price.
        discount_amount (Decimal): Calculated discount amount (regular_price - price).
        in_stock (bool): Boolean indicating if product is in stock and available.
    Note:
        This is an abstract model (Meta.abstract = True) and will not create
        a database table. It should be inherited by concrete product models.
        Categories are specifically tailored for computer hardware and peripherals,
        including CPU, GPU, RAM, storage devices, and accessories.
        Warranty choices range from 1 year to lifetime warranty options.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=200, blank=True, null=True, help_text="Product name"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, help_text="Price in BDT"
    )
    regular_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Regular price in BDT",
    )
    brand = models.CharField(
        max_length=50, blank=True, null=True, help_text="Brand of the product"
    )
    model = models.CharField(
        max_length=100, blank=True, null=True, help_text="Model name of the product"
    )
    warranty = models.CharField(
        max_length=50,
        choices=[
            ("1 Year", "1 Year"),
            ("2 Years", "2 Years"),
            ("3 Years", "3 Years"),
            ("4 Years", "4 Years"),
            ("5 Years", "5 Years"),
            ("10 Years", "10 Years"),
            ("Lifetime Warranty", "Lifetime Warranty"),
        ],
        blank=True,
        null=True,
        help_text="Warranty duration",
    )
    description = models.TextField(blank=True, help_text="Description of the product")
    category = models.CharField(
        max_length=50,
        choices=[
            ("CPU", "CPU"),
            ("Cooler", "Cooler"),
            ("Motherboard", "Motherboard"),
            ("RAM", "RAM"),
            ("SSD", "SSD"),
            ("HDD", "HDD"),
            ("GPU", "GPU"),
            ("Power Supply", "Power Supply"),
            ("Casing", "Casing"),
            ("Monitor", "Monitor"),
            ("Keyboard", "Keyboard"),
            ("Mouse", "Mouse"),
            ("Headphone", "Headphone"),
        ],
        blank=True,
        null=True,
        help_text="Category of the product",
    )
    tdp = models.IntegerField(
        blank=True, null=True, help_text="Thermal Design Power (TDP) in watts"
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_featured = models.BooleanField(default=False, help_text="Featured product")
    is_new_arrival = models.BooleanField(default=False, help_text="New arrival product")
    is_on_sale = models.BooleanField(default=False, help_text="Product on sale")
    stock = models.PositiveIntegerField(default=0, help_text="Available stock quantity")
    is_available = models.BooleanField(
        default=True, help_text="Product availability status"
    )

    @property
    def discount_percentage(self):
        if self.regular_price and self.price and self.price < self.regular_price:
            return round(
                100 * (self.regular_price - self.price) / self.regular_price, 2
            )
        return 0

    @property
    def discount_amount(self):
        if self.regular_price and self.price:
            return self.regular_price - self.price
        return 0

    @property
    def in_stock(self):
        return self.stock > 0 and self.is_available

    class Meta:
        abstract = True  # This model won't be created as a table


class CPU(BaseProduct):
    """
    Django model representing a CPU (Central Processing Unit) product.
    This model extends BaseProduct to provide CPU-specific fields including images,
    technical specifications, and metadata. It's designed for e-commerce applications
    where CPU products need to be catalogued with detailed technical information.
    Attributes:
        image1-image5 (ImageField): Up to 5 product images stored in 'cpu_images/' directory.
            image1 serves as the main product image, while others are optional.
        socket (CharField): CPU socket type with predefined choices including Intel LGA
            sockets (1200, 1700, 1851) and AMD sockets (AM4, AM5, TR4).
        cores (IntegerField): Number of physical CPU cores, validated between 1-128.
        threads (IntegerField): Number of CPU threads (logical processors), validated
            between 1-256. Usually equals cores for non-hyperthreaded CPUs or 2x cores
            for hyperthreaded processors.
        base_frequency (FloatField): Base operating frequency in GHz, validated
            between 0.1-10.0 GHz.
        boost_frequency (FloatField): Maximum boost frequency in GHz, validated
            between 0.1-10.0 GHz. Represents peak performance under optimal conditions.
        cache (IntegerField): Total CPU cache size in MB, validated between 1-1024 MB.
            Includes all cache levels (L1, L2, L3).
        processor_graphics (CharField): Integrated graphics description (e.g.,
            "Intel UHD Graphics 770", "AMD Radeon Graphics").
    Methods:
        __str__(): Returns a formatted string representation. If core count, thread count,
            and boost frequency are available, returns detailed format:
            "Brand Model (XC/YT) Z.Z GHz". Otherwise returns basic "Brand Model" format.
        save(): Overrides parent save method to automatically set category to "CPU"
            before saving to database.
    Meta:
        verbose_name: "CPU" - Human-readable singular name for admin interface
        verbose_name_plural: "CPUs" - Human-readable plural name for admin interface
    Note:
        All technical specification fields are optional (blank=True, null=True) to
        accommodate incomplete product information. Validators ensure data integrity
        when values are provided.
    """

    # Image fields
    image1 = models.ImageField(
        upload_to="cpu_images/",
        blank=True,
        null=True,
        help_text="Image of the CPU (main)",
    )
    image2 = models.ImageField(
        upload_to="cpu_images/",
        blank=True,
        null=True,
        help_text="Image of the CPU (optional)",
    )
    image3 = models.ImageField(
        upload_to="cpu_images/",
        blank=True,
        null=True,
        help_text="Image of the CPU (optional)",
    )
    image4 = models.ImageField(
        upload_to="cpu_images/",
        blank=True,
        null=True,
        help_text="Image of the CPU (optional)",
    )
    image5 = models.ImageField(
        upload_to="cpu_images/",
        blank=True,
        null=True,
        help_text="Image of the CPU (optional)",
    )

    # Technical specifications
    socket = models.CharField(
        max_length=50,
        choices=[
            ("LGA 1200", "LGA 1200"),
            ("LGA 1700", "LGA 1700"),
            ("LGA 1851", "LGA 1851"),
            ("AM4", "AM4"),
            ("AM5", "AM5"),
            ("TR4", "TR4"),
        ],
        blank=True,
        null=True,
        help_text="CPU socket type",
    )
    cores = models.IntegerField(
        blank=True,
        null=True,
        help_text="Number of CPU cores",
        validators=[MinValueValidator(1), MaxValueValidator(128)],
    )
    threads = models.IntegerField(
        blank=True,
        null=True,
        help_text="Number of CPU threads",
        validators=[MinValueValidator(1), MaxValueValidator(256)],
    )
    base_frequency = models.FloatField(
        blank=True,
        null=True,
        help_text="Base frequency in GHz",
        validators=[MinValueValidator(0.1), MaxValueValidator(10.0)],
    )
    boost_frequency = models.FloatField(
        blank=True,
        null=True,
        help_text="Boost frequency in GHz",
        validators=[MinValueValidator(0.1), MaxValueValidator(10.0)],
    )
    cache = models.IntegerField(
        blank=True,
        null=True,
        help_text="Cache size in MB",
        validators=[MinValueValidator(1), MaxValueValidator(1024)],
    )
    processor_graphics = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Integrated graphics (e.g., Intel UHD, AMD Radeon)",
    )

    class Meta:
        verbose_name = "CPU"
        verbose_name_plural = "CPUs"

    def __str__(self):
        if self.cores and self.threads and self.boost_frequency:
            return f"{self.brand} {self.model} ({self.cores}C/{self.threads}T) {self.boost_frequency} GHz"
        else:
            return f"{self.brand} {self.model}"

    def save(self, *args, **kwargs):
        self.category = "CPU"
        super().save(*args, **kwargs)


class Cooler(BaseProduct):
    """
    Django model representing a computer cooling system product.
    This model extends BaseProduct to store specific information about CPU coolers,
    including both air and liquid cooling solutions. It captures technical specifications
    such as cooling performance, noise levels, RGB lighting capabilities, and socket
    compatibility.
    Attributes:
        image1 (ImageField): Primary product image stored in 'cooler_images/' directory.
        image2 (ImageField): Optional secondary product image.
        image3 (ImageField): Optional tertiary product image.
        image4 (ImageField): Optional quaternary product image.
        image5 (ImageField): Optional fifth product image.
        cooler_type (CharField): Type of cooling solution - 'Air Cooler' or 'Liquid Cooler'.
        cooler_size (CharField): Physical dimensions of the cooler (120mm to 480mm).
        fan_speed (IntegerField): Maximum fan rotation speed in RPM (300-5000).
        noise_level (IntegerField): Operating noise level in decibels (0-60 dB).
        rgb (BooleanField): Indicates presence of RGB lighting features.
        tdp (IntegerField): Thermal Design Power rating in watts (0-500W).
        socket_support (CharField): Comma-separated list of supported CPU socket types.
    Methods:
        __str__(): Returns formatted string with brand, model, and cooler type.
        save(): Automatically sets category to 'Cooler' before saving to database.
    Meta:
        verbose_name: Human-readable singular name for admin interface.
        verbose_name_plural: Human-readable plural name for admin interface.
    Example:
        Creating a new cooler instance:
        >>> cooler = Cooler(
        ...     brand="Noctua",
        ...     model="NH-D15",
        ...     cooler_type="Air Cooler",
        ...     cooler_size="140 mm",
        ...     fan_speed=1500,
        ...     noise_level=25,
        ...     rgb=False,
        ...     tdp=220,
        ...     socket_support="AM4, LGA1151, LGA1200"
        ... )
        >>> cooler.save()
    """

    image1 = models.ImageField(
        upload_to="cooler_images/",
        blank=True,
        null=True,
        help_text="Image of the Cooler (main)",
    )
    image2 = models.ImageField(
        upload_to="cooler_images/",
        blank=True,
        null=True,
        help_text="Image of the Cooler (optional)",
    )
    image3 = models.ImageField(
        upload_to="cooler_images/",
        blank=True,
        null=True,
        help_text="Image of the Cooler (optional)",
    )
    image4 = models.ImageField(
        upload_to="cooler_images/",
        blank=True,
        null=True,
        help_text="Image of the Cooler (optional)",
    )
    image5 = models.ImageField(
        upload_to="cooler_images/",
        blank=True,
        null=True,
        help_text="Image of the Cooler (optional)",
    )
    cooler_type = models.CharField(
        max_length=50,
        choices=[
            ("Air Cooler", "Air Cooler"),
            ("Liquid Cooler", "Liquid Cooler"),
        ],
        blank=True,
        null=True,
        help_text="Cooler Type",
    )
    cooler_size = models.CharField(
        max_length=50,
        choices=[
            ("120 mm", "120 mm"),
            ("140 mm", "140 mm"),
            ("240 mm", "240 mm"),
            ("280 mm", "280 mm"),
            ("360 mm", "360 mm"),
            ("420 mm", "420 mm"),
            ("480 mm", "480 mm"),
        ],
        blank=True,
        null=True,
        help_text="Cooler size",
    )
    fan_speed = models.IntegerField(
        blank=True,
        null=True,
        help_text="Fan speed in RPM",
        validators=[MinValueValidator(300), MaxValueValidator(5000)],
    )
    noise_level = models.IntegerField(
        blank=True,
        null=True,
        help_text="Noise level in dB",
        validators=[MinValueValidator(0), MaxValueValidator(60)],
    )
    rgb = models.BooleanField(
        blank=True,
        null=True,
        help_text="RGB lighting",
    )
    tdp = models.IntegerField(
        blank=True,
        null=True,
        help_text="Thermal Design Power (TDP) in watts",
        validators=[MinValueValidator(0), MaxValueValidator(500)],
    )
    socket_support = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Supported CPU sockets (comma separated)",
    )

    class Meta:
        verbose_name = "Cooler"
        verbose_name_plural = "Coolers"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.cooler_type or 'Cooler'})"

    def save(self, *args, **kwargs):
        self.category = "Cooler"
        super().save(*args, **kwargs)


class Motherboard(BaseProduct):
    """
    Django model representing a computer motherboard product.
    This model extends BaseProduct to include motherboard-specific attributes such as
    form factor, socket type, chipset, memory specifications, expansion slots, and
    connectivity options. It's designed for e-commerce applications dealing with
    computer hardware.
    Attributes:
        image1-image5 (ImageField): Up to 5 product images stored in 'motherboard_images/' directory.
            image1 serves as the main product image, while image2-5 are optional additional views.
        form_factor (CharField): Physical size and layout standard of the motherboard.
            Choices include ATX, Micro-ATX, Mini-ITX, and E-ATX form factors.
        socket (CharField): CPU socket type that determines processor compatibility.
            Supports Intel sockets (LGA 1200, 1700, 1851) and AMD sockets (AM4, AM5, TR4).
        chipset (CharField): Motherboard chipset that defines features and capabilities.
            Includes Intel chipsets (H510, B460, H610, B660, B760, Z790, Z890) and
            AMD chipsets (A520, B450, B550, X570, A620, B650, X670, X670E, X870, X870E, TRX40).
        memory_slots (IntegerField): Number of RAM slots available on the motherboard.
        memory_type (CharField): Type of RAM supported (DDR4 or DDR5).
        max_memory (CharField): Maximum RAM capacity supported, ranging from 32 GB to 2 TB.
        pcie_slots (IntegerField): Number of PCIe expansion slots for graphics cards and other components.
        m2_slots (IntegerField): Number of M.2 slots for NVMe SSDs and other M.2 devices.
        sata_ports (IntegerField): Number of SATA ports for connecting storage devices.
        usb_ports (IntegerField): Total number of USB ports available.
        wifi_bluetooth (BooleanField): Whether the motherboard has built-in Wi-Fi and Bluetooth support.
    Methods:
        __str__: Returns a formatted string with brand, model, socket, chipset, and form factor.
        save: Automatically sets the category to "Motherboard" before saving to database.
    Meta:
        verbose_name: Human-readable singular name for admin interface.
        verbose_name_plural: Human-readable plural name for admin interface.
    Note:
        All fields except memory_type are optional (blank=True, null=True) to accommodate
        varying levels of product specification detail. The model automatically categorizes
        itself as "Motherboard" upon saving.
    """

    image1 = models.ImageField(
        upload_to="motherboard_images/",
        blank=True,
        null=True,
        help_text="Image of the Motherboard (main)",
    )
    image2 = models.ImageField(
        upload_to="motherboard_images/",
        blank=True,
        null=True,
        help_text="Image of the Motherboard (optional)",
    )
    image3 = models.ImageField(
        upload_to="motherboard_images/",
        blank=True,
        null=True,
        help_text="Image of the Motherboard (optional)",
    )
    image4 = models.ImageField(
        upload_to="motherboard_images/",
        blank=True,
        null=True,
        help_text="Image of the Motherboard (optional)",
    )
    image5 = models.ImageField(
        upload_to="motherboard_images/",
        blank=True,
        null=True,
        help_text="Image of the Motherboard (optional)",
    )
    form_factor = models.CharField(
        max_length=50,
        choices=[
            ("ATX", "ATX"),
            ("Micro-ATX", "Micro-ATX"),
            ("Mini-ITX", "Mini-ITX"),
            ("E-ATX", "E-ATX"),
        ],
        blank=True,
        null=True,
        help_text="Form factor",
    )
    socket = models.CharField(
        max_length=50,
        choices=[
            ("LGA 1200", "LGA 1200"),
            ("LGA 1700", "LGA 1700"),
            ("LGA 1851", "LGA 1851"),
            ("AM4", "AM4"),
            ("AM5", "AM5"),
            ("TR4", "TR4"),
        ],
        blank=True,
        null=True,
        help_text="Socket",
    )
    chipset = models.CharField(
        max_length=50,
        choices=[
            ("H510", "H510"),
            ("B460", "B460"),
            ("H610", "H610"),
            ("B660", "B660"),
            ("B760", "B760"),
            ("Z790", "Z790"),
            ("Z890", "Z890"),
            ("A520", "A520"),
            ("B450", "B450"),
            ("B550", "B550"),
            ("X570", "X570"),
            ("A620", "A620"),
            ("B650", "B650"),
            ("X670", "X670"),
            ("X670E", "X670E"),
            ("X870", "X870"),
            ("X870E", "X870E"),
            ("TRX40", "TRX40"),
        ],
        blank=True,
        null=True,
        help_text="Chipset",
    )
    memory_slots = models.IntegerField(
        blank=True,
        null=True,
        help_text="Number of memory slots",
    )
    memory_type = models.CharField(
        max_length=50,
        choices=[
            ("DDR4", "DDR4"),
            ("DDR5", "DDR5"),
        ],
        help_text="Type of RAM",
    )
    max_memory = models.CharField(
        max_length=10,
        choices=[
            ("32 GB", "32 GB"),
            ("64 GB", "64 GB"),
            ("128 GB", "128 GB"),
            ("256 GB", "256 GB"),
            ("512 GB", "512 GB"),
            ("1 TB", "1 TB"),
            ("2 TB", "2 TB"),
        ],
        blank=True,
        null=True,
        help_text="Maximum memory capacity",
    )
    pcie_slots = models.IntegerField(
        blank=True,
        null=True,
        help_text="Number of PCIe slots",
    )
    m2_slots = models.IntegerField(
        blank=True,
        null=True,
        help_text="Number of M.2 slots",
    )
    sata_ports = models.IntegerField(
        blank=True,
        null=True,
        help_text="Number of SATA ports",
    )
    usb_ports = models.IntegerField(
        blank=True,
        null=True,
        help_text="Number of USB ports",
    )
    wifi_bluetooth = models.BooleanField(
        blank=True,
        null=True,
        help_text="Wi-Fi and Bluetooth support",
    )

    class Meta:
        verbose_name = "Motherboard"
        verbose_name_plural = "Motherboards"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.socket}) {self.chipset} {self.form_factor}"

    def save(self, *args, **kwargs):
        self.category = "Motherboard"
        super().save(*args, **kwargs)


class RAM(BaseProduct):
    """
    Django model representing RAM (Random Access Memory) products.
    This model extends BaseProduct to provide specific fields and functionality
    for RAM components. It includes comprehensive specifications such as memory
    type, capacity, frequency, and multiple image storage capabilities.
    Attributes:
        image1 (ImageField): Primary product image stored in ram_images/ directory.
        image2 (ImageField): Optional secondary product image.
        image3 (ImageField): Optional tertiary product image.
        image4 (ImageField): Optional quaternary product image.
        image5 (ImageField): Optional fifth product image.
        ram_class (CharField): Classification of RAM usage (Desktop/Laptop/Server).
        ram_type (CharField): Memory technology type (DDR3, DDR4, DDR5, etc.).
        memory_capacity (CharField): Storage capacity in gigabytes (4GB to 64GB).
        frequency (CharField): Operating frequency in MHz (1333MHz to 8000MHz).
    Meta:
        verbose_name: Human-readable name for the model (RAM).
        verbose_name_plural: Plural form for admin interface (RAMs).
    Methods:
        __str__(): Returns formatted string representation including brand, model,
                  capacity, and RAM type.
        save(): Overrides parent save method to automatically set category to "RAM".
    Usage:
        Used in Django admin and application views to manage RAM product inventory,
        specifications, and display information for e-commerce or catalog systems.
    """

    image1 = models.ImageField(
        upload_to="ram_images/",
        blank=True,
        null=True,
        help_text="Image of the RAM (main)",
    )
    image2 = models.ImageField(
        upload_to="ram_images/",
        blank=True,
        null=True,
        help_text="Image of the RAM (optional)",
    )
    image3 = models.ImageField(
        upload_to="ram_images/",
        blank=True,
        null=True,
        help_text="Image of the RAM (optional)",
    )
    image4 = models.ImageField(
        upload_to="ram_images/",
        blank=True,
        null=True,
        help_text="Image of the RAM (optional)",
    )
    image5 = models.ImageField(
        upload_to="ram_images/",
        blank=True,
        null=True,
        help_text="Image of the RAM (optional)",
    )
    ram_class = models.CharField(
        max_length=50,
        choices=[
            ("Desktop", "Desktop"),
            ("Laptop", "Laptop"),
            ("Server", "Server"),
        ],
        blank=True,
        null=True,
        help_text="Type of RAM",
    )
    ram_type = models.CharField(
        max_length=50,
        choices=[
            ("DDR3", "DDR3"),
            ("DDR4", "DDR4"),
            ("DDR5", "DDR5"),
            ("LPDDR3", "LPDDR3"),
            ("LPDDR4", "LPDDR4"),
            ("LPDDR5", "LPDDR5"),
            ("ECC DDR4", "ECC DDR4"),
            ("ECC DDR5", "ECC DDR5"),
        ],
        help_text="Type of RAM",
    )
    memory_capacity = models.CharField(
        max_length=10,
        choices=[
            ("4 GB", "4 GB"),
            ("8 GB", "8 GB"),
            ("16 GB", "16 GB"),
            ("32 GB", "32 GB"),
            ("64 GB", "64 GB"),
        ],
        blank=True,
        null=True,
        help_text="RAM capacity",
    )
    frequency = models.CharField(
        max_length=50,
        choices=[
            ("1333 MHz", "1333 MHz"),
            ("1600 MHz", "1600 MHz"),
            ("1866 MHz", "1866 MHz"),
            ("2133 MHz", "2133 MHz"),
            ("2400 MHz", "2400 MHz"),
            ("2666 MHz", "2666 MHz"),
            ("3000 MHz", "3000 MHz"),
            ("3200 MHz", "3200 MHz"),
            ("3600 MHz", "3600 MHz"),
            ("4000 MHz", "4000 MHz"),
            ("4266 MHz", "4266 MHz"),
            ("4400 MHz", "4400 MHz"),
            ("4600 MHz", "4600 MHz"),
            ("4800 MHz", "4800 MHz"),
            ("5000 MHz", "5000 MHz"),
            ("5200 MHz", "5200 MHz"),
            ("5400 MHz", "5400 MHz"),
            ("5600 MHz", "5600 MHz"),
            ("5800 MHz", "5800 MHz"),
            ("6000 MHz", "6000 MHz"),
            ("6400 MHz", "6400 MHz"),
            ("6800 MHz", "6800 MHz"),
            ("7200 MHz", "7200 MHz"),
            ("7400 MHz", "7400 MHz"),
            ("7600 MHz", "7600 MHz"),
            ("7800 MHz", "7800 MHz"),
            ("8000 MHz", "8000 MHz"),
        ],
        blank=True,
        null=True,
        help_text="Frequency",
    )

    class Meta:
        verbose_name = "RAM"
        verbose_name_plural = "RAMs"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.memory_capacity}) {self.ram_type}"

    def save(self, *args, **kwargs):
        self.category = "RAM"
        super().save(*args, **kwargs)


class SSD(BaseProduct):
    """
    Django model representing a Solid State Drive (SSD) product.
    This model extends BaseProduct to include SSD-specific attributes such as
    storage capacity, form factor, interface type, and performance metrics.
    Supports multiple product images and various SSD configurations commonly
    found in the market.
    Attributes:
        image1 (ImageField): Primary product image stored in 'ssd_images/' directory.
        image2-image5 (ImageField): Optional additional product images for gallery display.
        storage_capacity (CharField): Storage capacity with predefined choices ranging
            from 120 GB to 8 TB. Allows blank/null values for incomplete entries.
        form_factor (CharField): Physical form factor (2.5-inch, M.2, PCIe Add-in Card).
            Determines compatibility with different system configurations.
        interface (CharField): Connection interface type (SATA III, PCIe 3.0/4.0 variants).
            Affects data transfer capabilities and system compatibility.
        read_speed (IntegerField): Sequential read performance in MB/s. Optional field
            for performance specifications.
        write_speed (IntegerField): Sequential write performance in MB/s. Optional field
            for performance specifications.
    Meta:
        verbose_name: Singular display name in Django admin.
        verbose_name_plural: Plural display name in Django admin.
    Methods:
        __str__: Returns formatted string combining brand and model for object representation.
    Note:
        All image fields use 'ssd_images/' upload directory for organized file storage.
        Performance fields (read_speed, write_speed) are integers representing MB/s values.
        Choice fields use tuple format for database value and human-readable display.
    """

    image1 = models.ImageField(
        upload_to="ssd_images/",
        blank=True,
        null=True,
        help_text="Image of the SSD (main)",
    )
    image2 = models.ImageField(
        upload_to="ssd_images/",
        blank=True,
        null=True,
        help_text="Image of the SSD (optional)",
    )
    image3 = models.ImageField(
        upload_to="ssd_images/",
        blank=True,
        null=True,
        help_text="Image of the SSD (optional)",
    )
    image4 = models.ImageField(
        upload_to="ssd_images/",
        blank=True,
        null=True,
        help_text="Image of the SSD (optional)",
    )
    image5 = models.ImageField(
        upload_to="ssd_images/",
        blank=True,
        null=True,
        help_text="Image of the SSD (optional)",
    )
    storage_capacity = models.CharField(
        max_length=10,
        choices=[
            ("120 GB", "120 GB"),
            ("240 GB", "240 GB"),
            ("256 GB", "256 GB"),
            ("480 GB", "480 GB"),
            ("512 GB", "512 GB"),
            ("1 TB", "1 TB"),
            ("2 TB", "2 TB"),
            ("4 TB", "4 TB"),
            ("8 TB", "8 TB"),
        ],
        blank=True,
        null=True,
        help_text="Storage capacity",
    )
    form_factor = models.CharField(
        max_length=50,
        choices=[
            ("2.5-inch", "2.5-inch"),
            ("M.2", "M.2"),
            ("PCIe Add-in Card", "PCIe Add-in Card"),
        ],
        blank=True,
        null=True,
        help_text="Form factor",
    )
    interface = models.CharField(
        max_length=50,
        choices=[
            ("SATA III", "SATA III"),
            ("PCIe 3.0 x4", "PCIe 3.0 x4"),
            ("PCIe 4.0 x4", "PCIe 4.0 x4"),
            ("PCIe 4.0 x8", "PCIe 4.0 x8"),
        ],
        blank=True,
        null=True,
        help_text="Interface",
    )
    read_speed = models.IntegerField(
        blank=True, null=True, help_text="Read speed in MB/s"
    )
    write_speed = models.IntegerField(
        blank=True, null=True, help_text="Write speed in MB/s"
    )

    class Meta:
        verbose_name = "SSD"
        verbose_name_plural = "SSDs"

    def __str__(self):
        return f"{self.brand} {self.model}"


class HDD(BaseProduct):
    """
    Django model representing a Hard Disk Drive (HDD) product.
    This model extends BaseProduct to include HDD-specific attributes such as storage
    capacity, form factor, interface type, rotational speed, and cache size. It supports
    multiple product images and provides predefined choices for common HDD specifications.
    Attributes:
        image1 (ImageField): Primary product image uploaded to 'hdd_images/' directory.
        image2-image5 (ImageField): Optional additional product images for comprehensive
            product display.
        storage_capacity (CharField): HDD storage capacity with predefined choices ranging
            from 500 GB to 18 TB. Limited to 10 characters.
        form_factor (CharField): Physical size specification, either 2.5-inch or 3.5-inch.
            Limited to 50 characters.
        interface (CharField): Connection interface type, supporting SATA II and SATA III.
            Limited to 50 characters.
        rpm (CharField): Rotational speed of the HDD platters, either 5400 RPM or 7200 RPM.
            Limited to 50 characters.
        cache (IntegerField): Cache buffer size in megabytes for improved performance.
    Meta:
        verbose_name: Singular form display name as 'HDD'.
        verbose_name_plural: Plural form display name as 'HDDs'.
    Methods:
        __str__(): Returns a string representation combining brand and model for easy
            identification in admin interface and queries.
    Note:
        All fields except those inherited from BaseProduct are optional (blank=True, null=True)
        to accommodate various product data availability scenarios.
    """

    image1 = models.ImageField(
        upload_to="hdd_images/",
        blank=True,
        null=True,
        help_text="Image of the HDD (main)",
    )
    image2 = models.ImageField(
        upload_to="hdd_images/",
        blank=True,
        null=True,
        help_text="Image of the HDD (optional)",
    )
    image3 = models.ImageField(
        upload_to="hdd_images/",
        blank=True,
        null=True,
        help_text="Image of the HDD (optional)",
    )
    image4 = models.ImageField(
        upload_to="hdd_images/",
        blank=True,
        null=True,
        help_text="Image of the HDD (optional)",
    )
    image5 = models.ImageField(
        upload_to="hdd_images/",
        blank=True,
        null=True,
        help_text="Image of the HDD (optional)",
    )
    storage_capacity = models.CharField(
        max_length=10,
        choices=[
            ("500 GB", "500 GB"),
            ("1 TB", "1 TB"),
            ("2 TB", "2 TB"),
            ("4 TB", "4 TB"),
            ("6 TB", "6 TB"),
            ("8 TB", "8 TB"),
            ("10 TB", "10 TB"),
            ("12 TB", "12 TB"),
            ("14 TB", "14 TB"),
            ("16 TB", "16 TB"),
            ("18 TB", "18 TB"),
        ],
        blank=True,
        null=True,
        help_text="Storage capacity",
    )
    form_factor = models.CharField(
        max_length=50,
        choices=[
            ("2.5-inch", "2.5-inch"),
            ("3.5-inch", "3.5-inch"),
        ],
        blank=True,
        null=True,
        help_text="Form factor",
    )
    interface = models.CharField(
        max_length=50,
        choices=[
            ("SATA II", "SATA II"),
            ("SATA III", "SATA III"),
        ],
        blank=True,
        null=True,
        help_text="Interface",
    )
    rpm = models.CharField(
        max_length=50,
        choices=[
            ("5400 RPM", "5400 RPM"),
            ("7200 RPM", "7200 RPM"),
        ],
        blank=True,
        null=True,
        help_text="Rotational speed",
    )
    cache = models.IntegerField(blank=True, null=True, help_text="Cache size in MB")

    class Meta:
        verbose_name = "HDD"
        verbose_name_plural = "HDDs"

    def __str__(self):
        return f"{self.brand} {self.model}"


class GPU(BaseProduct):
    """
    GPU model representing graphics processing units in the product catalog.
    This model extends BaseProduct to store detailed information about graphics cards
    including specifications like memory, clock speeds, display outputs, and power
    requirements. It's designed for e-commerce applications selling computer hardware.
    Attributes:
        image1 (ImageField): Primary product image for the GPU.
        image2-5 (ImageField): Additional optional product images.
        memory_type (CharField): Type of GPU memory (DDR3, GDDR5, GDDR5X, GDDR6, GDDR6X).
        vram_capacity (CharField): Video memory capacity ranging from 2GB to 32GB.
        max_resolution (CharField): Maximum supported display resolution.
        core_clock (FloatField): GPU core clock speed in MHz.
        memory_clock (FloatField): Memory clock speed in MHz.
        cores (IntegerField): Number of processing cores in the GPU.
        memory_bus (CharField): Memory bus width (64-bit to 512-bit).
        memory_interface (CharField): PCIe interface version (3.0, 4.0, 5.0).
        core_type (CharField): Type of processing cores (CUDA, Stream Processors, etc.).
        dp_ports (CharField): Number of DisplayPort outputs (1-4).
        hdmi_ports (CharField): Number of HDMI outputs (1-4).
        vga_ports (CharField): Number of VGA outputs (1-4).
        dvi_ports (CharField): Number of DVI outputs (1-4).
        connectors (CharField): Power connector requirements (6-pin, 8-pin, etc.).
    Methods:
        __str__(): Returns a formatted string with brand, model, and VRAM capacity.
    Usage:
        This model is used to catalog GPU products with comprehensive technical
        specifications for online retail platforms or inventory management systems.
    """

    image1 = models.ImageField(
        upload_to="gpu_images/",
        blank=True,
        null=True,
        help_text="Image of the GPU (main)",
    )
    image2 = models.ImageField(
        upload_to="gpu_images/",
        blank=True,
        null=True,
        help_text="Image of the GPU (optional)",
    )
    image3 = models.ImageField(
        upload_to="gpu_images/",
        blank=True,
        null=True,
        help_text="Image of the GPU (optional)",
    )
    image4 = models.ImageField(
        upload_to="gpu_images/",
        blank=True,
        null=True,
        help_text="Image of the GPU (optional)",
    )
    image5 = models.ImageField(
        upload_to="gpu_images/",
        blank=True,
        null=True,
        help_text="Image of the GPU (optional)",
    )
    memory_type = models.CharField(
        max_length=50,
        choices=[
            ("DDR3", "DDR3"),
            ("GDDR5", "GDDR5"),
            ("GDDR5X", "GDDR5X"),
            ("GDDR6", "GDDR6"),
            ("GDDR6X", "GDDR6X"),
        ],
        blank=True,
        null=True,
        help_text="Type of GPU memory",
    )
    vram_capacity = models.CharField(
        max_length=10,
        choices=[
            ("2 GB", "2 GB"),
            ("4 GB", "4 GB"),
            ("6 GB", "6 GB"),
            ("8 GB", "8 GB"),
            ("12 GB", "12 GB"),
            ("16 GB", "16 GB"),
            ("24 GB", "24 GB"),
            ("32 GB", "32 GB"),
        ],
        blank=True,
        null=True,
        help_text="VRAM capacity",
    )
    max_resolution = models.CharField(
        max_length=50, blank=True, null=True, help_text="Max supported resolution"
    )
    core_clock = models.FloatField(
        blank=True, null=True, help_text="Core clock speed in MHz"
    )
    memory_clock = models.FloatField(
        blank=True, null=True, help_text="Memory clock speed in MHz"
    )
    cores = models.IntegerField(
        blank=True,
        null=True,
        help_text="Number of GPU cores",
    )
    memory_bus = models.CharField(
        max_length=50,
        choices=[
            ("64-bit", "64-bit"),
            ("128-bit", "128-bit"),
            ("192-bit", "192-bit"),
            ("256-bit", "256-bit"),
            ("384-bit", "384-bit"),
            ("448-bit", "448-bit"),
            ("512-bit", "512-bit"),
        ],
        blank=True,
        null=True,
        help_text="Memory bus width",
    )
    memory_interface = models.CharField(
        max_length=20,
        choices=[
            ("PCI Express 3.0", "PCI Express 3.0"),
            ("PCI Express 4.0", "PCI Express 4.0"),
            ("PCI Express 5.0", "PCI Express 5.0"),
        ],
        blank=True,
        null=True,
        help_text="Memory interface",
    )
    core_type = models.CharField(
        max_length=50,
        choices=[
            ("CUDA Cores", "CUDA Cores"),
            ("Stream Processors", "Stream Processors"),
            ("RDNA Cores", "RDNA Cores"),
            ("Xe Cores", "Xe Cores"),
        ],
        blank=True,
        null=True,
        help_text="Type of GPU cores",
    )
    dp_ports = models.CharField(
        max_length=50,
        choices=[
            ("DisplayPort x1", "DisplayPort x1"),
            ("DisplayPort x2", "DisplayPort x2"),
            ("DisplayPort x3", "DisplayPort x3"),
            ("DisplayPort x4", "DisplayPort x4"),
        ],
        blank=True,
        null=True,
        help_text="DisplayPort ports",
    )
    hdmi_ports = models.CharField(
        max_length=50,
        choices=[
            ("HDMI x1", "HDMI x1"),
            ("HDMI x2", "HDMI x2"),
            ("HDMI x3", "HDMI x3"),
            ("HDMI x4", "HDMI x4"),
        ],
        blank=True,
        null=True,
        help_text="HDMI ports",
    )
    vga_ports = models.CharField(
        max_length=50,
        choices=[
            ("VGA x1", "VGA x1"),
            ("VGA x2", "VGA x2"),
            ("VGA x3", "VGA x3"),
            ("VGA x4", "VGA x4"),
        ],
        blank=True,
        null=True,
        help_text="VGA ports",
    )
    dvi_ports = models.CharField(
        max_length=50,
        choices=[
            ("DVI x1", "DVI x1"),
            ("DVI x2", "DVI x2"),
            ("DVI x3", "DVI x3"),
            ("DVI x4", "DVI x4"),
        ],
        blank=True,
        null=True,
        help_text="DVI ports",
    )
    connectors = models.CharField(
        max_length=50,
        choices=[
            ("6 Pin Connector", "6 Pin Connector"),
            ("8 Pin Connector", "8 Pin Connector"),
            ("8+8 Pin Connector", "8+8 Pin Connector"),
            ("16 Pin Connector", "16 Pin Connector"),
        ],
        blank=True,
        null=True,
        help_text="Power connectors",
    )

    class Meta:
        verbose_name = "GPU"
        verbose_name_plural = "GPUs"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.vram_capacity})"


class PowerSupply(BaseProduct):
    """
    Django model representing a Power Supply Unit (PSU) product.
    This model extends BaseProduct to include PSU-specific attributes such as
    wattage, efficiency ratings, modularity, and form factors. It supports
    multiple image uploads and provides standardized choices for common PSU
    specifications.
    Attributes:
        image1 (ImageField): Primary image of the PSU, uploaded to 'psu_images/' directory.
        image2-image5 (ImageField): Optional additional images of the PSU.
        form_factor (CharField): Physical form factor of the PSU (ATX, SFX).
        wattage (IntegerField): Power output capacity in watts.
        efficiency (CharField): 80 Plus efficiency certification level.
        modularity (CharField): Cable management type (Non-Modular, Semi-Modular, Fully Modular).
        fan_size (CharField): Cooling fan diameter in millimeters.
    Meta:
        verbose_name: Human-readable singular name for admin interface.
        verbose_name_plural: Human-readable plural name for admin interface.
    Methods:
        __str__: Returns formatted string with brand, model, and wattage for object representation.
    Example:
        >>> psu = PowerSupply(brand="Corsair", model="RM850x", wattage=850)
        >>> str(psu)
        'Corsair RM850x (850W)'
    """

    image1 = models.ImageField(
        upload_to="psu_images/",
        blank=True,
        null=True,
        help_text="Image of the PSU (main)",
    )
    image2 = models.ImageField(
        upload_to="psu_images/",
        blank=True,
        null=True,
        help_text="Image of the PSU (optional)",
    )
    image3 = models.ImageField(
        upload_to="psu_images/",
        blank=True,
        null=True,
        help_text="Image of the PSU (optional)",
    )
    image4 = models.ImageField(
        upload_to="psu_images/",
        blank=True,
        null=True,
        help_text="Image of the PSU (optional)",
    )
    image5 = models.ImageField(
        upload_to="psu_images/",
        blank=True,
        null=True,
        help_text="Image of the PSU (optional)",
    )
    form_factor = models.CharField(
        max_length=50,
        choices=[
            ("ATX", "ATX"),
            ("SFX", "SFX"),
        ],
        blank=True,
        null=True,
        help_text="Form factor",
    )
    wattage = models.IntegerField(
        blank=True,
        null=True,
        help_text="Wattage",
    )
    efficiency = models.CharField(
        max_length=50,
        choices=[
            ("80 Plus", "80 Plus"),
            ("80 Plus White", "80 Plus White"),
            ("80 Plus Bronze", "80 Plus Bronze"),
            ("80 Plus Silver", "80 Plus Silver"),
            ("80 Plus Gold", "80 Plus Gold"),
            ("80 Plus Platinum", "80 Plus Platinum"),
            ("80 Plus Titanium", "80 Plus Titanium"),
        ],
        blank=True,
        null=True,
        help_text="Efficiency rating",
    )
    modularity = models.CharField(
        max_length=50,
        choices=[
            ("Non-Modular", "Non-Modular"),
            ("Semi-Modular", "Semi-Modular"),
            ("Fully Modular", "Fully Modular"),
        ],
        blank=True,
        null=True,
        help_text="Modularity",
    )
    fan_size = models.CharField(
        max_length=50,
        choices=[
            ("80 mm", "80 mm"),
            ("92 mm", "92 mm"),
            ("120 mm", "120 mm"),
            ("140 mm", "140 mm"),
            ("200 mm", "200 mm"),
        ],
        blank=True,
        null=True,
        help_text="Fan size",
    )

    class Meta:
        verbose_name = "Power Supply"
        verbose_name_plural = "Power Supplies"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.wattage}W)"


class Casing(BaseProduct):
    """
    Django model representing computer casing/case products.
    This model extends BaseProduct to store detailed information about computer cases,
    including physical specifications, supported components, and features. It provides
    comprehensive tracking of case attributes for inventory and product management systems.
    Attributes:
        image1-image5 (ImageField): Product images with main image and optional additional views
        type (CharField): Case size category (Full Tower, Mid Tower, etc.)
        form_factor (CharField): Motherboard compatibility (ATX, Micro-ATX, Mini-ITX, E-ATX)
        side_panel (CharField): Side panel material (Tempered Glass, Solid, Plastic, Mesh)
        ssd_bays (IntegerField): Number of solid state drive mounting bays
        hdd_bays (IntegerField): Number of hard disk drive mounting bays
        expansion_slots (IntegerField): Number of PCIe expansion card slots
        fan_support (CharField): Maximum supported fan size (80mm to 200mm)
        radiator_support (CharField): Maximum supported radiator size (120mm to 480mm)
        rgb (BooleanField): Whether the case includes RGB lighting features
        dust_filters (BooleanField): Whether the case includes dust filtration
        cable_management (BooleanField): Whether the case has cable management features
        power_supply (BooleanField): Whether a power supply is included
        pre_installed_fans (IntegerField): Number of fans pre-installed in the case
    Meta:
        verbose_name: Display name for single instance
        verbose_name_plural: Display name for multiple instances
    Methods:
        __str__: Returns formatted string with brand, model, and form factor
    Note:
        All fields except inherited BaseProduct fields are optional (blank=True, null=True)
        to accommodate varying product specifications and incomplete data scenarios.
    """

    image1 = models.ImageField(
        upload_to="casing_images/",
        blank=True,
        null=True,
        help_text="Image of the Casing (main)",
    )
    image2 = models.ImageField(
        upload_to="casing_images/",
        blank=True,
        null=True,
        help_text="Image of the Casing (optional)",
    )
    image3 = models.ImageField(
        upload_to="casing_images/",
        blank=True,
        null=True,
        help_text="Image of the Casing (optional)",
    )
    image4 = models.ImageField(
        upload_to="casing_images/",
        blank=True,
        null=True,
        help_text="Image of the Casing (optional)",
    )
    image5 = models.ImageField(
        upload_to="casing_images/",
        blank=True,
        null=True,
        help_text="Image of the Casing (optional)",
    )
    type = models.CharField(
        max_length=50,
        choices=[
            ("Full Tower", "Full Tower"),
            ("Mid Tower", "Mid Tower"),
            ("Mini Tower", "Mini Tower"),
            ("Micro Tower", "Micro Tower"),
            ("Ultra Slim", "Ultra Slim"),
        ],
        blank=True,
        null=True,
        help_text="Type of case",
    )
    form_factor = models.CharField(
        max_length=50,
        choices=[
            ("ATX", "ATX"),
            ("Micro-ATX", "Micro-ATX"),
            ("Mini-ITX", "Mini-ITX"),
            ("E-ATX", "E-ATX"),
        ],
        blank=True,
        null=True,
        help_text="Form factor",
    )
    side_panel = models.CharField(
        max_length=50,
        choices=[
            ("Tempered Glass", "Tempered Glass"),
            ("Solid", "Solid"),
            ("Plastic", "Plastic"),
            ("Mesh", "Mesh"),
        ],
        blank=True,
        null=True,
        help_text="Side panel",
    )
    ssd_bays = models.IntegerField(
        blank=True,
        null=True,
        help_text="Number of SSD bays",
    )
    hdd_bays = models.IntegerField(
        blank=True,
        null=True,
        help_text="Number of HDD bays",
    )
    expansion_slots = models.IntegerField(
        blank=True,
        null=True,
        help_text="Number of expansion slots",
    )
    fan_support = models.CharField(
        max_length=50,
        choices=[
            ("80 mm", "80 mm"),
            ("92 mm", "92 mm"),
            ("120 mm", "120 mm"),
            ("140 mm", "140 mm"),
            ("200 mm", "200 mm"),
        ],
        blank=True,
        null=True,
        help_text="Fan support",
    )
    radiator_support = models.CharField(
        max_length=50,
        choices=[
            ("120 mm", "120 mm"),
            ("140 mm", "140 mm"),
            ("240 mm", "240 mm"),
            ("280 mm", "280 mm"),
            ("360 mm", "360 mm"),
            ("420 mm", "420 mm"),
            ("480 mm", "480 mm"),
        ],
        blank=True,
        null=True,
        help_text="Radiator support",
    )
    rgb = models.BooleanField(
        blank=True,
        null=True,
        help_text="RGB lighting",
    )
    dust_filters = models.BooleanField(
        blank=True,
        null=True,
        help_text="Dust filters",
    )
    cable_management = models.BooleanField(
        blank=True,
        null=True,
        help_text="Cable management",
    )
    power_supply = models.BooleanField(
        blank=True,
        null=True,
        help_text="With power supply",
    )
    pre_installed_fans = models.IntegerField(
        blank=True,
        null=True,
        help_text="Number of pre-installed fans",
    )

    class Meta:
        verbose_name = "Casing"
        verbose_name_plural = "Casings"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.form_factor})"


class Monitor(BaseProduct):
    """
    Django model representing a computer monitor product.
    This model extends BaseProduct to include monitor-specific attributes such as
    display specifications, connectivity options, and performance characteristics.
    It provides comprehensive fields for storing technical details about monitors
    including screen properties, port configurations, and multimedia features.
    Attributes:
        image1-image5 (ImageField): Product images uploaded to 'monitor_images/' directory.
            image1 serves as the main product image, while image2-image5 are optional
            additional images for showcasing different angles or features.
        screen_resolution (CharField): Display resolution with predefined choices ranging
            from HD (1280x720) to 8K (7680x4320), including ultrawide formats.
        aspect_ratio (CharField): Screen aspect ratio with choices of 16:9 (standard),
            21:9 (ultrawide), or 32:9 (super ultrawide).
        screen_size (CharField): Physical screen size diagonal measurement in inches,
            supporting common monitor sizes from 18" to 38".
        vga_ports (CharField): Number of VGA (Video Graphics Array) ports available,
            supporting 1-4 ports for legacy analog video connections.
        hdmi_ports (CharField): Number of HDMI (High-Definition Multimedia Interface)
            ports, supporting 1-4 ports for digital audio/video transmission.
        dp_ports (CharField): Number of DisplayPort connections available, supporting
            1-4 ports for high-bandwidth digital display interface.
        dvi_ports (CharField): Number of DVI (Digital Visual Interface) ports,
            supporting 1-4 ports for digital video connections.
        usb_c_ports (CharField): Number of USB-C ports available, supporting 1-4 ports
            for modern connectivity and potential display/power delivery.
        usb_ports (CharField): Number of standard USB ports, supporting 1-4 ports
            for peripheral connectivity and USB hub functionality.
        speakers (BooleanField): Indicates whether the monitor has built-in speakers
            for audio output without external speakers.
        refresh_rate (IntegerField): Display refresh rate measured in Hz, indicating
            how many times per second the screen updates the image.
        response_time (IntegerField): Pixel response time measured in milliseconds,
            indicating how quickly pixels can change colors (important for gaming).
        brightness (IntegerField): Maximum brightness level measured in cd/m²
            (candelas per square meter), indicating display luminance capability.
    Meta:
        verbose_name: Human-readable singular name for admin interface.
        verbose_name_plural: Human-readable plural name for admin interface.
    Methods:
        __str__: Returns a string representation combining brand, model, screen size,
            and resolution for easy identification in admin lists and debugging.
    Usage:
        This model is typically used in e-commerce applications for computer hardware
        retailers to catalog monitor products with detailed technical specifications
        that help customers make informed purchasing decisions.
    """

    image1 = models.ImageField(
        upload_to="monitor_images/",
        blank=True,
        null=True,
        help_text="Image of the Monitor (main)",
    )
    image2 = models.ImageField(
        upload_to="monitor_images/",
        blank=True,
        null=True,
        help_text="Image of the Monitor (optional)",
    )
    image3 = models.ImageField(
        upload_to="monitor_images/",
        blank=True,
        null=True,
        help_text="Image of the Monitor (optional)",
    )
    image4 = models.ImageField(
        upload_to="monitor_images/",
        blank=True,
        null=True,
        help_text="Image of the Monitor (optional)",
    )
    image5 = models.ImageField(
        upload_to="monitor_images/",
        blank=True,
        null=True,
        help_text="Image of the Monitor (optional)",
    )
    screen_resolution = models.CharField(
        max_length=25,
        choices=[
            ("1280 x 720", "1280 x 720"),
            ("1920 x 1080", "1920 x 1080"),
            ("2560 x 1440", "2560 x 1440"),
            ("3840 x 2160", "3840 x 2160"),
            ("7680 x 4320", "7680 x 4320"),
            ("2560 x 1080", "2560 x 1080"),
            ("3440 x 1440", "3440 x 1440"),
            ("5120 x 2160", "5120 x 2160"),
            ("5120 x 1440", "5120 x 1440"),
        ],
        blank=True,
        null=True,
        help_text="Screen Resolution",
    )
    aspect_ratio = models.CharField(
        max_length=25,
        choices=[
            ("16:9", "16:9"),
            ("21:9", "21:9"),
            ("32:9", "32:9"),
        ],
        blank=True,
        null=True,
        help_text="Aspect Ratio",
    )
    screen_size = models.CharField(
        max_length=50,
        choices=[
            ("18-inch", "18-inch"),
            ("22-inch", "22-inch"),
            ("24-inch", "24-inch"),
            ("32-inch", "32-inch"),
            ("29-inch", "29-inch"),
            ("34-inch", "34-inch"),
            ("38-inch", "38-inch"),
        ],
        blank=True,
        null=True,
        help_text="Screen Size",
    )
    vga_ports = models.CharField(
        max_length=50,
        choices=[
            ("VGA x1", "VGA x1"),
            ("VGA x2", "VGA x2"),
            ("VGA x3", "VGA x3"),
            ("VGA x4", "VGA x4"),
        ],
        blank=True,
        null=True,
        help_text="VGA ports",
    )
    hdmi_ports = models.CharField(
        max_length=50,
        choices=[
            ("HDMI x1", "HDMI x1"),
            ("HDMI x2", "HDMI x2"),
            ("HDMI x3", "HDMI x3"),
            ("HDMI x4", "HDMI x4"),
        ],
        blank=True,
        null=True,
        help_text="HDMI ports",
    )
    dp_ports = models.CharField(
        max_length=50,
        choices=[
            ("DisplayPort x1", "DisplayPort x1"),
            ("DisplayPort x2", "DisplayPort x2"),
            ("DisplayPort x3", "DisplayPort x3"),
            ("DisplayPort x4", "DisplayPort x4"),
        ],
        blank=True,
        null=True,
        help_text="DisplayPort ports",
    )
    dvi_ports = models.CharField(
        max_length=50,
        choices=[
            ("DVI x1", "DVI x1"),
            ("DVI x2", "DVI x2"),
            ("DVI x3", "DVI x3"),
            ("DVI x4", "DVI x4"),
        ],
        blank=True,
        null=True,
        help_text="DVI ports",
    )
    usb_c_ports = models.CharField(
        max_length=50,
        choices=[
            ("USB-C x1", "USB-C x1"),
            ("USB-C x2", "USB-C x2"),
            ("USB-C x3", "USB-C x3"),
            ("USB-C x4", "USB-C x4"),
        ],
        blank=True,
        null=True,
        help_text="USB-C ports",
    )
    usb_ports = models.CharField(
        max_length=50,
        choices=[
            ("USB x1", "USB x1"),
            ("USB x2", "USB x2"),
            ("USB x3", "USB x3"),
            ("USB x4", "USB x4"),
        ],
        blank=True,
        null=True,
        help_text="USB ports",
    )
    speakers = models.BooleanField(
        blank=True,
        null=True,
        help_text="Built-in speakers",
    )
    refresh_rate = models.IntegerField(
        blank=True,
        null=True,
        help_text="Refresh rate in Hz",
    )
    response_time = models.IntegerField(
        blank=True,
        null=True,
        help_text="Response time in ms",
    )
    brightness = models.IntegerField(
        blank=True,
        null=True,
        help_text="Brightness in cd/m²",
    )

    class Meta:
        verbose_name = "Monitor"
        verbose_name_plural = "Monitors"

    def __str__(self):
        return f"{self.brand} {self.model} {self.screen_size} {self.screen_resolution}"


class Keyboard(BaseProduct):
    """
    Django model representing a keyboard product.
    This model extends BaseProduct to include keyboard-specific attributes such as
    key type, interface, size, switch type, and other technical specifications.
    It supports multiple image uploads and various keyboard configurations.
    Attributes:
        image1 (ImageField): Primary keyboard image uploaded to 'keyboard_images/' directory.
        image2 (ImageField): Optional secondary keyboard image.
        image3 (ImageField): Optional tertiary keyboard image.
        image4 (ImageField): Optional quaternary keyboard image.
        image5 (ImageField): Optional fifth keyboard image.
        key_type (CharField): Type of keyboard keys - either 'Membrane' or 'Mechanical'.
        interface (CharField): Connection interface type including USB-A, PS-2, Wireless, or USB Type-C.
        keyboard_size (CharField): Physical size category of the keyboard ranging from 60% to full-size (100%).
        number_of_keys (IntegerField): Total count of keys on the keyboard.
        switch_type (CharField): Type of key switches used, applicable mainly for mechanical keyboards.
            Options include various colors (Blue, Red, Brown, etc.) and characteristics (Tactile, Clicky, Linear, etc.).
        cable_length (IntegerField): Length of the keyboard cable measured in meters.
        rgb (BooleanField): Indicates whether the keyboard has RGB lighting capabilities.
    Meta:
        verbose_name (str): Human-readable singular name for the model.
        verbose_name_plural (str): Human-readable plural name for the model.
    Methods:
        __str__(): Returns a string representation combining model, brand, and key type.
    Example:
        Creating a mechanical keyboard instance:
        >>> keyboard = Keyboard.objects.create(
        ...     model="K95 RGB",
        ...     brand="Corsair",
        ...     key_type="Mechanical",
        ...     interface="USB-A",
        ...     keyboard_size="Full-size Keyboard (100%)",
        ...     switch_type="Red",
        ...     rgb=True
        ... )
    """

    image1 = models.ImageField(
        upload_to="keyboard_images/",
        blank=True,
        null=True,
        help_text="Image of the Keyboard (main)",
    )
    image2 = models.ImageField(
        upload_to="keyboard_images/",
        blank=True,
        null=True,
        help_text="Image of the Keyboard (optional)",
    )
    image3 = models.ImageField(
        upload_to="keyboard_images/",
        blank=True,
        null=True,
        help_text="Image of the Keyboard (optional)",
    )
    image4 = models.ImageField(
        upload_to="keyboard_images/",
        blank=True,
        null=True,
        help_text="Image of the Keyboard (optional)",
    )
    image5 = models.ImageField(
        upload_to="keyboard_images/",
        blank=True,
        null=True,
        help_text="Image of the Keyboard (optional)",
    )
    key_type = models.CharField(
        max_length=20,
        choices=[
            ("Membrane", "Membrane"),
            ("Mechanical", "Mechanical"),
        ],
        blank=True,
        null=True,
        help_text="Key Types",
    )
    interface = models.CharField(
        max_length=50,
        choices=[
            ("USB-A", "USB-A"),
            ("PS-2", "PS-2"),
            ("Wireless", "Wireless"),
            ("USB Type-C", "USB Type-C"),
        ],
        blank=True,
        null=True,
        help_text="Interface",
    )
    keyboard_size = models.CharField(
        max_length=50,
        choices=[
            ("Full-size Keyboard (100%)", "Full-size Keyboard (100%)"),
            ("Tenkeyless Keyboard (TKL) (~87%)", "Tenkeyless Keyboard (TKL) (~87%)"),
            ("75% Keyboard (~75%)", "75% Keyboard (~75%)"),
            ("65% Keyboard (~65%)", "65% Keyboard (~65%)"),
            ("60% Keyboard (~60%)", "60% Keyboard (~60%)"),
        ],
        blank=True,
        null=True,
        help_text="Keyboard Size",
    )
    number_of_keys = models.IntegerField(
        blank=True,
        null=True,
        help_text="Number of keys",
    )
    switch_type = models.CharField(
        max_length=50,
        choices=[
            ("Standard", "Standard"),
            ("Blue", "Blue"),
            ("Red", "Red"),
            ("Brown", "Brown"),
            ("Yellow", "Yellow"),
            ("Green", "Green"),
            ("Silver", "Silver"),
            ("Silent", "Silent"),
            ("Tactile", "Tactile"),
            ("Clicky", "Clicky"),
            ("Linear", "Linear"),
            ("Speed", "Speed"),
            ("Optical", "Optical"),
        ],
        blank=True,
        null=True,
        help_text="Switch Type",
    )
    cable_length = models.IntegerField(
        blank=True,
        null=True,
        help_text="Cable length in meters",
    )
    rgb = models.BooleanField(
        blank=True,
        null=True,
        help_text="RGB lighting",
    )

    class Meta:
        verbose_name = "Keyboard"
        verbose_name_plural = "Keyboards"

    def __str__(self):
        return f"{self.model} {self.brand} ({self.key_type})"


class Mouse(BaseProduct):
    """
    A Django model representing a computer mouse product.
    This model extends BaseProduct to include mouse-specific attributes such as
    interface type, DPI settings, button configuration, and visual features.
    Supports multiple image uploads for comprehensive product display.
    Attributes:
        image1 (ImageField): Primary product image stored in 'mouse_images/' directory.
        image2-5 (ImageField): Optional secondary product images for additional views.
        mouse_type (CharField): Type of mouse mechanism - Membrane or Mechanical.
        interface (CharField): Connection interface (USB-A, PS-2, Wireless, USB Type-C).
        use_type (CharField): Intended usage category - Gaming or Office.
        number_of_buttons (IntegerField): Total count of mouse buttons.
        max_dpi (IntegerField): Maximum DPI (dots per inch) sensitivity setting.
        cable_length (IntegerField): Length of cable in appropriate units (if wired).
        rgb (BooleanField): Indicates presence of RGB lighting features.
    Meta:
        verbose_name: Human-readable singular name 'Mouse'.
        verbose_name_plural: Human-readable plural name 'Mice'.
    Methods:
        __str__(): Returns formatted string with brand, model, RGB status, and use type.
    Note:
        All fields except inherited BaseProduct fields are optional (blank=True, null=True)
        to accommodate varying product specifications and data availability.
    """

    image1 = models.ImageField(
        upload_to="mouse_images/",
        blank=True,
        null=True,
        help_text="Image of the Mouse (main)",
    )
    image2 = models.ImageField(
        upload_to="mouse_images/",
        blank=True,
        null=True,
        help_text="Image of the Mouse (optional)",
    )
    image3 = models.ImageField(
        upload_to="mouse_images/",
        blank=True,
        null=True,
        help_text="Image of the Mouse (optional)",
    )
    image4 = models.ImageField(
        upload_to="mouse_images/",
        blank=True,
        null=True,
        help_text="Image of the Mouse (optional)",
    )
    image5 = models.ImageField(
        upload_to="mouse_images/",
        blank=True,
        null=True,
        help_text="Image of the Mouse (optional)",
    )
    mouse_type = models.CharField(
        max_length=20,
        choices=[
            ("Membrane", "Membrane"),
            ("Mechanical", "Mechanical"),
        ],
        blank=True,
        null=True,
        help_text="Mouse Types",
    )
    interface = models.CharField(
        max_length=50,
        choices=[
            ("USB-A", "USB-A"),
            ("PS-2", "PS-2"),
            ("Wireless", "Wireless"),
            ("USB Type-C", "USB Type-C"),
        ],
        blank=True,
        null=True,
        help_text="Interface",
    )
    use_type = models.CharField(
        max_length=50,
        choices=[
            ("Gaming", "Gaming"),
            ("Office", "Office"),
        ],
        blank=True,
        null=True,
        help_text="Mouse Type",
    )
    number_of_buttons = models.IntegerField(
        blank=True,
        null=True,
        help_text="Number of buttons",
    )
    max_dpi = models.IntegerField(
        blank=True,
        null=True,
    )
    cable_length = models.IntegerField(
        blank=True,
        null=True,
    )
    rgb = models.BooleanField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Mouse"
        verbose_name_plural = "Mice"

    def __str__(self):
        return f"{self.brand} {self.model} {self.rgb} {self.use_type}"


class Headphone(BaseProduct):
    """
    Django model representing a Headphone product with detailed specifications.
    This model extends BaseProduct to include headphone-specific attributes such as
    audio specifications, connection types, and physical characteristics. It supports
    multiple image uploads and comprehensive product categorization.
    Attributes:
        image1-image5 (ImageField): Product images stored in headphone_images/ directory.
            image1 serves as the main product image, while image2-image5 are optional
            additional views.
        headphone_type (CharField): Category of headphone (Standard, Gaming, Studio,
            Professional) with 50 character limit.
        connection (CharField): Connection method - either Wired or Wireless.
        microphone (BooleanField): Indicates presence of built-in microphone.
        noise_cancellation (BooleanField): Indicates active noise cancellation capability.
        rgb (BooleanField): Indicates presence of RGB lighting features.
        frequency_response (CharField): Audio frequency range with predefined options
            (20 Hz - 20 kHz, 10 Hz - 40 kHz, 5 Hz - 50 kHz).
        impedance (IntegerField): Electrical impedance measurement in ohms.
        sensitivity (IntegerField): Audio sensitivity measurement in decibels (dB).
        input_jack (CharField): Physical connector type (3.5 mm, USB-A, USB-C).
        cable_length (IntegerField): Length of attached cable in meters (for wired models).
    Meta:
        verbose_name: Human-readable singular name "Headphone"
        verbose_name_plural: Human-readable plural name "Headphones"
    Methods:
        __str__(): Returns formatted string combining brand, model, and headphone type
            for easy identification in admin interface and debugging.
    Note:
        All fields except inherited BaseProduct fields are optional (blank=True, null=True)
        to accommodate varying product specifications and incomplete data scenarios.
    """

    image1 = models.ImageField(
        upload_to="headphone_images/",
        blank=True,
        null=True,
        help_text="Image of the Headphone (main)",
    )
    image2 = models.ImageField(
        upload_to="headphone_images/",
        blank=True,
        null=True,
        help_text="Image of the Headphone (optional)",
    )
    image3 = models.ImageField(
        upload_to="headphone_images/",
        blank=True,
        null=True,
        help_text="Image of the Headphone (optional)",
    )
    image4 = models.ImageField(
        upload_to="headphone_images/",
        blank=True,
        null=True,
        help_text="Image of the Headphone (optional)",
    )
    image5 = models.ImageField(
        upload_to="headphone_images/",
        blank=True,
        null=True,
        help_text="Image of the Headphone (optional)",
    )
    headphone_type = models.CharField(
        max_length=50,
        choices=[
            ("Standard", "Standard"),
            ("Gaming", "Gaming"),
            ("Studio", "Studio"),
            ("Professional", "Professional"),
        ],
        blank=True,
        null=True,
        help_text="Headphone Type",
    )
    connection = models.CharField(
        max_length=50,
        choices=[
            ("Wired", "Wired"),
            ("Wireless", "Wireless"),
        ],
        blank=True,
        null=True,
        help_text="Connection",
    )
    microphone = models.BooleanField(
        blank=True,
        null=True,
        help_text="Microphone",
    )
    noise_cancellation = models.BooleanField(
        blank=True,
        null=True,
        help_text="Noise Cancellation",
    )
    rgb = models.BooleanField(
        blank=True,
        null=True,
        help_text="RGB lighting",
    )
    frequency_response = models.CharField(
        max_length=50,
        choices=[
            ("20 Hz - 20 kHz", "20 Hz - 20 kHz"),
            ("10 Hz - 40 kHz", "10 Hz - 40 kHz"),
            ("5 Hz - 50 kHz", "5 Hz - 50 kHz"),
        ],
        blank=True,
        null=True,
        help_text="Frequency Response",
    )
    impedance = models.IntegerField(
        blank=True,
        null=True,
        help_text="Impedance in ohms",
    )
    sensitivity = models.IntegerField(
        blank=True,
        null=True,
        help_text="Sensitivity in dB",
    )
    input_jack = models.CharField(
        max_length=50,
        choices=[
            ("3.5 mm", "3.5 mm"),
            ("USB-A", "USB-A"),
            ("USB-C", "USB-C"),
        ],
        blank=True,
        null=True,
        help_text="Input Jack",
    )
    cable_length = models.IntegerField(
        blank=True,
        null=True,
        help_text="Cable length in meters",
    )

    class Meta:
        verbose_name = "Headphone"
        verbose_name_plural = "Headphones"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.headphone_type})"
