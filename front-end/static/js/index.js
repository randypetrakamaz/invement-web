// set active hamburger nav
function navClick(x) {
    if( window.innerWidth > 991){
        x.classList.toggle("active");
    }
}


var multiple_dataset = [
	{ stok:"20", stok2:"35", year:"Jan" },
	{ stok:"40", stok2:"24", year:"Feb" },
	{ stok:"44", stok2:"20", year:"Mar" },
	{ stok:"23", stok2:"50", year:"Apr" },
	{ stok:"21", stok2:"36", year:"Mei" },
	{ stok:"50", stok2:"40", year:"Jun" }
];


webix.ready(function(){

    // Grafik keluar masuk
    webix.ui({
        container: "graph-container",
        css: "round",
        rows:[
            { view:"template", template:"<p class='text-center'>Grafik Barang Keluar & Masuk</p>", type:"header", align: "center", borderless: true }, 
            { view:"chart",
                borderless: true,
                autowidth: true,
                height:220,
                type:"bar",
                barWidth:60,
                radius:2,
                gradient:"rising",
                xAxis:{
                    title: "Bulan",
                    template:"#year#"
                },
                yAxis:{
                    title: "Jumlah",
                    start:0,
                    step:10,
                    end:100
                },
                legend:{
                    values:[{text:"Laptop", color:"#58dccd"},{text:"Aksesoris",color:"#a7ee70"},{text:"Lain-lain",color:"#36abee"}],
                    valign:"middle",
                    align:"right",
                    width:90,
                    layout:"y"
                },
                series:[
                    {
                        value:"#stok#",
                        color: "#58dccd",
                        tooltip:{
                        template:"#stok#"
                        }
                    },
                    {
                        value:"#stok2#",
                        color:"#a7ee70",
                        tooltip:{
                        template:"#stok2#"
                        }
                    },
                ],
                data: multiple_dataset}
        ]
      });

    // variabel berisi tampilan tabel barang limit stok
    var tblLimit = {
        id: "tbl_barang",
        css:"webix_data_border webix_header_border",
        autowidth: true,
        autoheight: true,
        minHeight: 180,
        view: "datatable",
        url: "https://backend-randy-5zn7xh2gqq-et.a.run.app/data-barang",
        columns: [
            { id: "no",   header: "No",    width:50, template: function(obj) {
                var data = $$("tbl_barang");
                var index = data.getIndexById(obj.id);
                return index + 1;
              }
            },
            { id: "id",   header: "ID Barang" , width:90},
            { id: "barang",   header: "Nama Barang", width:180, maxWidth:  200},
            { id: "jenis",   header: "Jenis Barang", width: 120, maxWidth:150 },
            { id: "stok",   header: "Stok Barang", width:50},
        ],
        on:{
            // pesan saat sedang load data
            onBeforeLoad:function(){
                this.showOverlay("Loading...");
            },

            onAfterLoad:function(){
                // menutup overlay pesan loading
                this.hideOverlay();

                // Menampilkan pesan jika data tidak ada
                if(!this.count()) {
                    this.showOverlay("Maaf, data tidak tersedia");
                }

                // Menampilkan data dengan jumlah stok kurang dari lima
                this.filter(function(item){
                    return item.stok < 6;
                });
            }
        },
        pager: "pager"
    }

    // jalankan webix ui tabel stok limit
    webix.ui({
        container: "tabel-barang",
        rows: [
            tblLimit,
            {
                view:"pager",
                id:"pager",
                size:5,
                group:3,
                template:"{common.first()}{common.prev()}{common.pages()}{common.next()}{common.last()}"
            }
        ]        
    });
      

    // tabel aktivitas admin
    webix.ui({
        container: "tabel-aktivitas",
        rows:[
            {
                id: "tbl_aktivitas",
                css:"webix_data_border webix_header_border",
                autowidth: true,
                autoheight: true,
                minHeight: 180,
                view:"datatable",
                url: "https://backend-randy-5zn7xh2gqq-et.a.run.app/data-riwayat",
                columns:[
                    { id: "index",   header: "No",    width:45 },
                    { id: "tanggal",   
                      header: "Tanggal",     
                      maxWidth:100, 
                      template: 
                      //   ubah format tanggal
                      function(obj){
                        return webix.i18n.dateFormatStr(obj.tanggal, "%d %m %Y");
                      }
                    },
                    { id: "admin",   header: "Admin",         maxWidth:90},
                    { id: "aktivitas",   header: "Aktivitas", width: 175, maxWidth: 250, template: function(obj) {
                        var text = obj.aktivitas;
                        if (text.length > 15) {
                            text = text.substr(0, 18) + '...';
                        }
                        return text;
                    } }
                ],
                scheme:{
                    $init:function(obj){ obj.index = this.count(); }
                },
                on: {
                    // pesan saat sedang load data
                    onBeforeLoad:function(){
                        this.showOverlay("Loading...");
                    },

                    onAfterLoad:function(){
                        // menutup overlay pesan loading
                        this.hideOverlay();
                            
                        if(!this.count()) {
                        this.showOverlay("Maaf, tidak ada data tersedia");
                        }
                    }
                },
                pager: "pager1"
            },
            {
                view:"pager",
                id:"pager1",
                size:5,
                group:3,
                template:"{common.first()}{common.prev()}{common.pages()}{common.next()}{common.last()}"
            }
        ]
    });
});


