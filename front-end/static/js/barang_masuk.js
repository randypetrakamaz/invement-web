webix.ready(function(){
    webix.ui({
        container: "tabel",
        type: "space",
        rows:[
          { cols:[
              { view:"text", label:"Cari Data:", placeholder:"Id, tanggal, id barang, nama barang, dan jumlah", id:"filter-table", maxwidth: 300 },
              {}
            ]
          },
          { 
            id: "tabel",
            css:"webix_data_border webix_header_border",
            view: "datatable",
            autoheight: true,
            minHeight: 180,
            autowidth: true,
            url: "https://backend-randy-5zn7xh2gqq-et.a.run.app/data-barang-masuk",
            columns:[
                { id: "index",    header: "No",    sort: "int", maxWidth: 35 },
                { id: "id",  header: "Id", sort: "int" },
                { id: "tanggal",
                  header: "Tanggal", 
                  maxWidth: 180,
                  template: 
                    //   ubah format tanggal
                    function(obj){
                        return webix.i18n.dateFormatStr(obj.tanggal, "%d %m %Y");
                    }
                },
                { id: "id_barang",       header: "ID Barang" ,   sort: "string", maxWidth: 100 },
                { id: "barang",   header: "Nama Barang",  sort: "string", minWidth: 240 },
                { id: "stok",   header: "Jumlah",    sort: "int", maxWidth: 100},
                { id:"aksi", header:"Aksi", template: "{common.edit} {common.hapus}", maxWidth: 80, css: "pointer" }
            ],
            type: {
                edit: "<button class='edit'><i class='webix_icon wxi-pencil'></i></button>",
                hapus: "<button class='hapus'><i class='webix_icon wxi-trash'></i></button>"
            },
            onClick: {
                edit:function(){
                    // mengambil id dari row yang diklik tombol edit
                    var item_id = $$("tabel").getSelectedId();
                    // mengambil id dari data row yang diklik
                    var value = $$("tabel").getItem(item_id);
                    console.log(value)
                    if (item_id){
                        Edit(value);
                    }
                },
                hapus:function(){
                    var item_id = $$("tabel").getSelectedId();
                    var value = $$("tabel").getItem(item_id);
                    
                    if (item_id){
                        // menampilkan konfirmasi sebelum menghapus data
                        webix.confirm({
                        title: "Konfirmasi",
                        text: "Apakah anda yakin ingin menghapus data ini?",
                        ok:"Ya", cancel:"Tidak"
                        }).then(function(){
                            // mengirim request ke server untuk menghapus data
                            webix.send("/barang-masuk", {"id": value.id, "action": "hapus"}, "POST")
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

    $$("filter-table").attachEvent("onTimedKeypress", function(){
        var text = this.getValue().toString().toLowerCase();
        
        $$("tabel").filter(function(obj){
            //filter by multiple properties
            var filter = [obj.id_barang, obj.barang, obj.id, obj.tanggal, obj.stok].join("|");
            filter = filter.toString().toLowerCase();
            return (filter.indexOf(text) != -1);
        });
    });
});



var data = 'https://backend-randy-5zn7xh2gqq-et.a.run.app/data-barang';
var optionsData = [];

webix.ajax(data, function(text){
    var json = JSON.parse(text);

    // Iterasi data array
    for(var i = 0; i < json.length; i++){
        var item = json[i];

        // Membuat object untuk setiap item
        var option = {
            id: item.id,
            value: item.barang
        };

        // Menambahkan object ke array options
        optionsData.push(option);
    }
});


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
                            { view: "text", id: "id-barang", label: "Id barang", name: "id_barang", readonly: true },
                            {
                                view:"select",
                                id: "select-barang",
                                name:"nama_barang",
                                label:"Nama Barang",
                                options: optionsData,
                                on: {
                                    onChange:function(id){
                                        // mendapatkan nilai yang dipilih dari elemen select
                                        var selectedValue = this.getValue();
                                        // menetapkan nilai untuk kontrol teks
                                        $$("id-barang").setValue(selectedValue);
                                    }
                                }
                            },
                        ]
                    },
                    { width: 30 }, // menambahkan margin pada elemen layout
                    {
                        margin:10, //jarak antara child
                        rows: [
                            {
                                view: "datepicker",
                                label: "Tanggal Masuk",
                                inputWidth: 180,
                                labelWidth: 90,
                                format: "%Y-%d-%m",
                                name: "tanggal"
                            },
                            { view: "counter", label: "Jumlah", name: "jumlah" },
                        ]
                    }
                ]
            },
            { 
                view: "button", 
                value: "Simpan", 
                css:"webix_primary", 
                click: function(){
                    data = $$("tambah-form").getValues()
                    // data.tanggal = webix.i18n.parseFormatStr();
                    var date = new Date(data.tanggal);
                    var formattedDate = date.getFullYear() + "-" + (date.getMonth()+1).toString().padStart(2,'0') + "-" + date.getDate().toString().padStart(2,'0');
                    data.tanggal = formattedDate;
                    data.action = "tambah"
                    // Kode untuk menyimpan data ke database
                    webix.send("/barang-masuk", data, "POST");
                    form.hide();
                }
            }
        ],
        elementsConfig:{
            labelPosition:"top"
        }
    }
});
  
var addBtn = document.getElementById("btn-tambah");
addBtn.addEventListener("click", function(){
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
                            { view: "text", id: "id_barang", label: "Id barang", name: "id_barang", readonly: true },
                            {
                                view:"select",
                                id: "barang",
                                name:"nama_barang",
                                label:"Nama Barang",
                                options: optionsData,
                                on: {
                                    onChange:function(id){
                                        // mendapatkan nilai yang dipilih dari elemen select
                                        var selectedValue = this.getValue();
                                        // menetapkan nilai untuk kontrol teks
                                        $$("id_barang").setValue(selectedValue);
                                    }
                                }
                            },
                        ]
                    },
                    { width: 30 }, // menambahkan margin pada elemen layout
                    {
                        margin:10, //jarak antara child
                        rows: [
                            {
                                view: "datepicker",
                                label: "Tanggal Masuk",
                                inputWidth: 180,
                                labelWidth: 90,
                                format: "%Y-%d-%m",
                                name: "tanggal"
                            },
                            { view: "counter", label: "Jumlah", name: "jumlah" },
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
                    // Kode untuk menyimpan data ke database
                    webix.send("/barang-masuk", data, "POST");
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
    form.setValues(value);
    formEdit.show();
}
