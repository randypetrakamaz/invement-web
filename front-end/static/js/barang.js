webix.ready(function(){
    webix.ui({
        container: "tabel",
        type: "space",
        rows:[
            { cols:[
                { view:"text", label:"Cari Data:", placeholder:"Id, nama, dan jenis", id:"filter-table", maxwidth: 300 },
                {},
                { view:"text", type: "number", label: "Filter Data:", placeholder:"Stok", id:"filter-number", maxwidth: 250 }
              ]
            },
            { 
                id: "tbl-barang",
                css:"webix_data_border webix_header_border",
                view: "datatable",
                autoheight: true,
                minHeight: 180,
                autowidth: true,
                url: "https://backend-randy-5zn7xh2gqq-et.a.run.app/data-barang",
                columns:[
                    { id: "index",    header: "No",    sort: "int", maxWidth: 35 },
                    { id: "id",       header: "ID" ,   sort: "string", maxWidth: 50 },
                    { id: "barang",   header: "Nama",  sort: "string", minWidth: 240 },
                    { id: "jenis",    header: "Jenis" },
                    { id: "beli",   header: "Harga Beli", template: "Rp#beli#", maxWidth: 250, sort: "int" },
                    { id: "jual",   header: "Harga Jual", template: "Rp#jual#", maxWidth: 250, sort: "int" },
                    { id: "stok",   header: "Stok",    sort: "int", maxWidth: 50},
                    { id:"aksi", header:"Aksi", template: "{common.edit} {common.hapus}", maxWidth: 80, css: "pointer" }
                ],
                type: {
                    edit: "<button class='edit'><i class='webix_icon wxi-pencil'></i></button>",
                    hapus: "<button class='hapus'><i class='webix_icon wxi-trash'></i></button>"
                },
                onClick: {
                    edit:function(){
                        // mengambil id dari row yang diklik tombol edit
                        var item_id = $$("tbl-barang").getSelectedId();
                        // mengambil id dari data row yang diklik
                        var value = $$("tbl-barang").getItem(item_id);
                        if (item_id){
                            Edit(value);
                        }
                    },
                    hapus:function(){
                        var item_id = $$("tbl-barang").getSelectedId();
                        var value = $$("tbl-barang").getItem(item_id);

                        if (item_id){
                            // menampilkan konfirmasi sebelum menghapus data
                            webix.confirm({
                            title: "Konfirmasi",
                            text: "Apakah anda yakin ingin menghapus data ini?",
                            ok:"Ya", cancel:"Tidak"
                            }).then(function(){
                                // mengirim request ke server untuk menghapus data
                                webix.send("/barang", {"id": value.id, "action": "hapus"}, "POST")
                            })
                        }
                    }
                },
                scheme: {
                    $init:function(obj){ obj.index = this.count(); }
                },
                on: {
                    onBeforeLoad:function(){
                        this.showOverlay("Loading...");
                    },
                        
                    onAfterLoad: function() {
                        this.hideOverlay();
                        if(!this.count()) {
                            this.showOverlay("Maaf, data tidak tersedia");
                        }
                    }
                },
                select: true,
                pager: "pager",
            },
            {
                view:"pager",
                id:"pager",
                size:5,
                group:3,
                template:"{common.first()}{common.prev()}{common.pages()}{common.next()}{common.last()}"
            }
        ]
    });

    // filter nama barang, id, jenis
    $$("filter-table").attachEvent("onTimedKeypress", function(){
        // ambil input dan ubah menjadi string lowercase
        var text = this.getValue().toString().toLowerCase();

        $$("tbl-barang").filter(function(obj){
            //filter by multiple properties
            var filter = [obj.barang, obj.id, obj.jenis].join("|");
            filter = filter.toString().toLowerCase();
            return (filter.indexOf(text) != -1);
        });
    });

    // filter stok
    $$("filter-number").attachEvent("onTimedKeypress", function(){
        
        var inputStok = this.getValue();
        
        $$("tbl-barang").filter(function(obj){
            if(inputStok === "" || inputStok === null){
                return obj;
            }
            return obj.stok < inputStok;
        });
    });    
});

    

// ================================= FORM TAMBAH DATA ===========================================
var form = webix.ui({
    view: "window",
    head: "Tambah Data",
    width: 450,
    autowidth: true,
    autoheight: true,
    position:"top",
    padding: -70, 
    modal: true,
    close: true,
    body: {
        view: "form",
        id: "tambah-form",
        padding: 30,
        margin: 40, //jarak antara child
        elements: [
            {
                view: "layout", 
                cols: [
                    {
                        margin:10, //jarak antara child
                        rows: [
                            { view: "text", label: "ID", name: "id" }, 
                            { view: "text", label: "Nama barang", name: "barang" },
                            { view: "text", label: "Jenis", name: "jenis" },
                        ]
                    },
                    { width: 30 }, // menambahkan margin pada elemen layout
                    {
                        margin:10,
                        rows: [
                            { view: "text", label: "Harga beli", name: "beli" },
                            { view: "text", label: "Harga jual", name: "jual" },
                            { view: "counter", label: "Stok", name: "stok" },
                        ]
                    }
                ]
            },
            { 
                view: "button", 
                value: "Simpan", 
                css:"webix_primary", 
                click: function(){
                    // ambil semua values form
                    data = $$("tambah-form").getValues()
                    // tambah key action dengan value tambah
                    data.action = "tambah"
                    // kirim data untuk disimpan data ke database
                    webix.send("/barang", data, "POST");
                    form.hide();
                }
            }
        ],
        elementsConfig:{
            labelPosition:"top"
        }
    }
});
  
// cari id btn-tambah
var addBtn = document.getElementById("btn-tambah");
// tambah event click
addBtn.addEventListener("click", function(){
    // tampilkan form tambah
    form.show();
});

  

// ================================= FORM EDIT DATA ===========================================
var formEdit = webix.ui({
    view: "window",
    id: "edit-window",
    head: "Edit Data",
    width: 450,
    autowidth: true,
    autoheight: true,
    position:"top",
    padding: -70, 
    modal: true,
    close: true,
    body: {
        view: "form",
        id: "form-edit",
        padding: 30,
        margin: 40, //jarak antara child
        elements: [
            {
                view: "layout", 
                cols: [
                    {
                        margin:10, //jarak antara child
                        rows: [
                            { view: "text", label: "ID", name: "id", readonly: true }, 
                            { view: "text", label: "Nama barang", name: "barang" },
                            { view: "text", label: "Jenis", name: "jenis" },
                        ]
                    },
                    { width: 30 }, // menambahkan margin pada elemen layout
                    {
                        margin:10,
                        rows: [
                            { view: "text", label: "Harga beli", name: "beli" },
                            { view: "text", label: "Harga jual", name: "jual" },
                            { view: "counter", label: "Stok", name: "stok" },
                        ]
                    }
                ]
            },
            { 
                view: "button", 
                value: "Ubah", 
                css:"webix_primary", 
                click: function(){
                    var data = $$('form-edit').getValues();
                    data.action = "edit";
                    
                    webix.send("/barang", data, "POST");
                    form.hide();
                }
            }
        ],
        elementsConfig:{
            labelPosition:"top"
        }
    }
});


function Edit(value) {
    var form = $$("form-edit");
    form.clear();
    // set values ke form edit
    form.setValues(value);
    formEdit.show();
}
