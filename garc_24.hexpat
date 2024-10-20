enum LanguageCode : u32 {
  LANG_ALL          =  0,
  LANG_JAPAN        =  1,
  LANG_ENGLISH      =  2,
  LANG_FRANCE       =  3,
  LANG_ITALY        =  4,
  LANG_GERMANY      =  5,
  LANG_SPAIN        =  7,
  LANG_KOREA        =  8,
  LANG_RUSSIA       =  9,
  LANG_NETHERLANDS  = 10,
  LANG_PORTUGAL     = 11,

};


struct Header {
      char signature[4];
      u32 block_size;
};

struct FileHeader{
Header header;
u16 byte_order;
u16 version;
u16 block_num;
u16 pad;
u32 total_block_size;
u32 file_size;
if(version > 516)
    u32 max_data_size;
};
struct FileAllocationOffsetBlock{
Header header;
u16 file_id_num;
u16 pad;
u32 offsets[file_id_num];//I point from after the header of FATB + count
};

  struct AllocationTableElement {
    u32 file_top;//Offset of file
    u32 file_bottom;//Stop reading here
  };

struct TableBlock{
LanguageCode language_bit;
AllocationTableElement element;
};

struct FileAllocationTableBlock{
Header header;
u32 file_id_num;
TableBlock blocks[file_id_num];
};
struct FileImageBlock{
Header header;
u32 image_size; //Size of entire data
};
struct GARC{
FileHeader hdr;
FileAllocationOffsetBlock faob;
FileAllocationTableBlock fatb;
FileImageBlock fib;
};

GARC file @ 0;