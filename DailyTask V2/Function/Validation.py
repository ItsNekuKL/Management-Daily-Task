class ValidasiTeks:
    def is_valid_nama(self, nama):
        """Validasi Inputan nama hanya huruf dna spasi"""
        return all(char.isalpha() or char.isspace() for char in nama)

