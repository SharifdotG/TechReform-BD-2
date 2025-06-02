"""Django admin configuration for ProductsApp.

This module configures the Django admin interface for all product models
in the TechReform application. It provides administrative interfaces for
managing computer hardware components including CPUs, GPUs, storage devices,
peripherals, and other PC building components.

The admin classes are designed to provide an intuitive interface for
administrators to manage product inventory, specifications, and metadata.
"""

from django.contrib import admin
from .models import (
    CPU,
    Cooler,
    Motherboard,
    RAM,
    SSD,
    HDD,
    GPU,
    PowerSupply,
    Casing,
    Monitor,
    Keyboard,
    Mouse,
    Headphone,
)


@admin.register(CPU)
class CPUAdmin(admin.ModelAdmin):
    """Admin interface for CPU models.

    Provides administrative functionality for managing CPU products
    including processors from various manufacturers with detailed
    specifications and compatibility information.
    """

    pass


@admin.register(Cooler)
class CoolerAdmin(admin.ModelAdmin):
    """Admin interface for Cooler models.

    Manages cooling solutions including air coolers, liquid coolers,
    and thermal solutions for PC builds with compatibility and
    performance specifications.
    """

    pass


@admin.register(Motherboard)
class MotherboardAdmin(admin.ModelAdmin):
    """Admin interface for Motherboard models.

    Handles motherboard products with socket compatibility, chipset
    information, expansion slots, and connectivity features for
    PC building configurations.
    """

    pass


@admin.register(RAM)
class RAMAdmin(admin.ModelAdmin):
    """Admin interface for RAM models.

    Manages memory modules including DDR4, DDR5 and other memory
    types with capacity, speed, and timing specifications for
    system performance optimization.
    """

    pass


@admin.register(SSD)
class SSDAdmin(admin.ModelAdmin):
    """Admin interface for SSD models.

    Administers solid-state drive products including SATA, NVMe,
    and M.2 SSDs with capacity, speed, and interface specifications
    for storage solutions.
    """

    pass


@admin.register(HDD)
class HDDAdmin(admin.ModelAdmin):
    """Admin interface for HDD models.

    Manages traditional hard disk drives with capacity, RPM,
    cache size, and interface specifications for bulk storage
    and backup solutions.
    """

    pass


@admin.register(GPU)
class GPUAdmin(admin.ModelAdmin):
    """Admin interface for GPU models.

    Handles graphics processing units including gaming and
    professional GPUs with memory, performance specifications,
    and compatibility information for visual computing.
    """

    pass


@admin.register(PowerSupply)
class PowerSupplyAdmin(admin.ModelAdmin):
    """Admin interface for PowerSupply models.

    Manages power supply units with wattage, efficiency ratings,
    modular cable configurations, and certification standards
    for stable system power delivery.
    """

    pass


@admin.register(Casing)
class CasingAdmin(admin.ModelAdmin):
    """Admin interface for Casing models.

    Administers PC cases and enclosures with form factor support,
    expansion slots, cooling compatibility, and build quality
    specifications for housing PC components.
    """

    pass


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    """Admin interface for Monitor models.

    Manages display devices including gaming monitors, professional
    displays with resolution, refresh rate, panel technology,
    and connectivity specifications.
    """

    pass


@admin.register(Keyboard)
class KeyboardAdmin(admin.ModelAdmin):
    """Admin interface for Keyboard models.

    Handles input devices including mechanical, membrane, and
    wireless keyboards with switch types, layout configurations,
    and feature specifications for user interaction.
    """

    pass


@admin.register(Mouse)
class MouseAdmin(admin.ModelAdmin):
    """Admin interface for Mouse models.

    Manages pointing devices including gaming mice, office mice
    with sensor specifications, button configurations, and
    ergonomic features for precise input control.
    """

    pass


@admin.register(Headphone)
class HeadphoneAdmin(admin.ModelAdmin):
    """Admin interface for Headphone models.

    Administers audio devices including gaming headsets, studio
    headphones with driver specifications, frequency response,
    and connectivity options for audio experiences.
    """

    pass
