from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# Inisialisasi Ursina
app = Ursina()

# Material blok (tekstur)
texture = load_texture('white_cube')

# Warna blok yang bisa dipilih
block_colors = [color.brown, color.gray, color.yellow, color.green]
color_names = ['Coklat', 'Silver', 'Kuning', 'Hijau']
current_color_index = 0  # Indeks warna saat ini

# Label untuk menampilkan warna saat ini
color_label = Text(text=f'Warna: {color_names[current_color_index]}', scale=2, origin=(0,0), position=(0,0.4), enabled=False)

# Kelas untuk blok
class Voxel(Button):
    def __init__(self, position=(0,0,0), block_color=None, base=False):
        super().__init__(
            parent=scene,
            model='cube',
            texture=texture,
            color=block_color if block_color else color.color(0, 0, random.uniform(0.9, 1)),
            position=position,
            scale=1
        )
        self.base = base  # Menandai blok dasar
    
    def input(self, key):
        if self.hovered:  # Pastikan blok sedang dihover
            if key == 'right mouse down' and not self.base:  # Hapus blok dengan klik kanan kecuali blok dasar
                destroy(self)
            elif key == 'left mouse down':  # Tambah blok dengan klik kiri, gunakan warna yang dipilih
                Voxel(position=self.position + mouse.normal, block_color=block_colors[current_color_index])

# Membuat area blok dasar yang tidak bisa dihapus
for x in range(10):
    for z in range(10):
        Voxel(position=(x, 0, z), base=True)  # Blok dasar yang tidak bisa dihapus

# Pemain (kamera pertama)
player = FirstPersonController()

# Fungsi untuk menampilkan label warna sementara
def show_color_label():
    color_label.text = f'Warna: {color_names[current_color_index]}'
    color_label.enabled = True
    invoke(setattr, color_label, 'enabled', False, delay=2)

# Fungsi untuk menangani input tombol
def input(key):
    global current_color_index
    if key == 'r':  # Jika tombol 'R' ditekan, ubah warna blok yang akan dibuat
        current_color_index = (current_color_index + 1) % len(block_colors)
        print(f'Warna blok berubah menjadi: {color_names[current_color_index]}')
        show_color_label()

# Fungsi untuk mengecek apakah pemain jatuh
def update():
    if player.y < -10:  # Jika pemain jatuh di bawah batas tertentu
        player.position = (5, 10, 5)  # Muncul kembali di atas

# Menjalankan game
app.run()
