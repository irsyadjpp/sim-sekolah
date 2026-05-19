INSERT INTO trx_ppdb_admission_path (id, name, description, is_active) VALUES
  ('a8b411d3-356a-49c9-8d76-92b005123401', 'Zonasi', 'Penerimaan berdasarkan kedekatan domisili alamat rumah calon siswa dengan lokasi sekolah.', true),
  ('a8b411d3-356a-49c9-8d76-92b005123402', 'Afirmasi', 'Penerimaan dikhususkan bagi calon siswa dari keluarga ekonomi tidak mampu.', true),
  ('a8b411d3-356a-49c9-8d76-92b005123403', 'Prestasi', 'Penerimaan berdasarkan prestasi akademik maupun non-akademik siswa.', true),
  ('a8b411d3-356a-49c9-8d76-92b005123404', 'Perpindahan Orang Tua/Wali', 'Penerimaan untuk calon siswa yang mengikuti perpindahan tugas kedinasan orang tua/wali.', true)
ON CONFLICT (name) DO NOTHING;
