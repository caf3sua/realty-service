import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

# Ensure application path is included
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.core.security import hash_password

# Load environment variables
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "anh_duong_land")

if not MONGODB_URI:
    print("Error: MONGODB_URI is not set in environment variables.")
    exit(1)

# Seeding Data
developers = [
    {
        "_id": "dev-1",
        "name": "Masterise Homes",
        "logo": "https://s3-hcmc02.higiocloud.vn/intranet/logos/0aabde5297104d3fb5988d5962f4106e.png",
        "title": "Phong Cách Sống Hàng Hiệu",
        "description": "Nhà phát triển bất động sản hàng hiệu hàng đầu Việt Nam, hợp tác cùng các đối tác toàn cầu như Elie Saab, Marriott International. Kiến tạo giá trị sống trường tồn và dịch vụ quản lý chất lượng thế giới.",
        "slug": "masterise-homes",
        "linkText": "Xem Các Căn Hộ Masterise Homes"
    },
    {
        "_id": "dev-2",
        "name": "MIK Group",
        "logo": "https://s3-hcmc02.higiocloud.vn/intranet/logos/1078c53f86aa4101adba8ebb6cf5ae80.png",
        "title": "Chuẩn Mực Sống Sang Trọng",
        "description": "Nổi tiếng với định vị dòng sản phẩm hạng sang The Matrix One và Imperia, MIK Group kiến tạo các giá trị sống bền vững, thiết kế xanh hài hòa thiên nhiên kết hợp công nghệ thông minh thời thượng.",
        "slug": "mik-group",
        "linkText": "Xem Các Căn Hộ MIK Group"
    },
    {
        "_id": "dev-3",
        "name": "Vinhomes",
        "logo": "https://s3-hcmc02.higiocloud.vn/intranet/logos/814d34d8c44d417494d5eacd8bfda06c.png",
        "title": "Đại Đô Thị Biển Quốc Tế",
        "description": "Thương hiệu bất động sản số 1 Việt Nam, nổi bật với các siêu dự án đô thị sinh thái kết hợp biển hồ nhân tạo kỳ vĩ, quy hoạch đồng bộ \"Tất cả trong một\" kiến tạo chuẩn mực sống văn minh hiện đại hàng đầu.",
        "slug": "vinhomes",
        "linkText": "Xem Các Sản Phẩm Vinhomes"
    },
    {
        "_id": "dev-4",
        "name": "Sun Group",
        "logo": "https://s3-hcmc02.higiocloud.vn/intranet/logos/804933c49a964efe815b86b12d6ef9da.png",
        "title": "Kiệt Tác Nghỉ Dưỡng Độc Bản",
        "description": "Tập đoàn hàng đầu trong phát triển bất động sản gắn liền với du lịch nghỉ dưỡng cao cấp, shophouse phong cách nghệ thuật Địa Trung Hải và các dinh thiện biển tráng lệ hòa mình cùng thiên nhiên kỳ vĩ.",
        "slug": "sun-group",
        "linkText": "Xem Các Sản Phẩm Sun Group"
    }
]

projects = [
    {
        "_id": "proj-1",
        "name": "Vinhomes Ocean Park 1",
        "slug": "ocean-park-1",
        "location": "Gia Lâm, Hà Nội",
        "developer": "Vinhomes",
        "shortDescription": "Thành phố Biển hồ - Nơi mang biển xanh cát trắng vào lòng Hà Nội với hồ nước mặn nhân tạo rộng lớn.",
        "description": "Vinhomes Ocean Park 1 sở hữu đại tiện ích độc đáo gồm Biển hồ nước mặn 6,1ha và Hồ Ngọc Trai cát trắng 24,5ha. Dự án được quy hoạch đồng bộ mang tầm cỡ quốc tế, cung cấp đa dạng dòng sản phẩm từ căn hộ chung cư cao cấp đến các căn biệt thự, liền kề, shophouse đẳng cấp.",
        "image": "https://s3-hcmc02.higiocloud.vn/intranet/logos/a0bbaaf456e241018de94bfdac6f5801.png",
        "banner": "https://s3-hcmc02.higiocloud.vn/intranet/logos/a9319aca6c8e44168ba033da3ea78419.png",
        "status": "Đã bàn giao",
        "scale": "420 ha",
        "priceRange": "2.5 tỷ - 120 tỷ",
        "tags": ["Biển hồ nhân tạo", "Hồ nước ngọt lớn", "Gia Lâm", "Vinhomes"]
    },
    {
        "_id": "proj-2",
        "name": "Vinhomes Ocean Park 2",
        "slug": "ocean-park-2",
        "location": "Văn Giang, Hưng Yên",
        "developer": "Vinhomes",
        "shortDescription": "Kinh đô Ánh sáng - Siêu quần thể đô thị biển quy mô 1.000 ha với công viên sóng Royal Wave Park quy mô nhất.",
        "description": "Vinhomes Ocean Park 2 (The Empire) là giai đoạn 2 của siêu quần thể đô thị biển Vinhomes, nổi bật với Tổ hợp công viên Biển tạo sóng nhân tạo Royal Wave Park lớn nhất thế giới (18ha). Dự án bao gồm các phân khu mang phong cách kiến trúc đa dạng từ Pháp, Ý, Địa Trung Hải đến Đông Dương.",
        "image": "https://s3-hcmc02.higiocloud.vn/intranet/logos/a8c4310ea0cc4c808edf7bcd0ef436cd.png",
        "banner": "https://s3-hcmc02.higiocloud.vn/intranet/logos/98645964f3d845d994b72096a0f37af8.png",
        "status": "Đang mở bán",
        "scale": "458 ha",
        "priceRange": "6 tỷ - 150 tỷ",
        "tags": ["Công viên sóng", "Kinh đô ánh sáng", "Biệt thự tân cổ điển", "Vinhomes"]
    },
    {
        "_id": "proj-3",
        "name": "Vinhomes Hạ Long Xanh",
        "slug": "ha-long-xanh",
        "location": "Quảng Yên & Hạ Long, Quảng Ninh",
        "developer": "Vinhomes",
        "shortDescription": "Đại đô thị sinh thái thông minh, vịnh biển kỳ quan của tương lai với quy mô hơn 4.100 ha.",
        "description": "Vinhomes Hạ Long Xanh là siêu dự án phức hợp mang tính biểu tượng tại Quảng Ninh. Tọa lạc tại vị trí vàng kết nối trực tiếp cao tốc Hải Phòng - Hạ Long, dự án tích hợp hệ sinh thái nghỉ dưỡng, sân golf 18 lỗ, công viên chủ đề Safari, bến du thuyền quốc tế và các khu đô thị sinh thái hiện đại bậc nhất châu Á.",
        "image": "https://s3-hcmc02.higiocloud.vn/intranet/logos/d97a42ce702747d4accfe16f57efbb68.png",
        "banner": "https://s3-hcmc02.higiocloud.vn/intranet/logos/aa3fb90a60004e9fb4f5d45f13cec943.png",
        "status": "Sắp mở bán",
        "scale": "4.109 ha",
        "priceRange": "Liên hệ",
        "tags": ["Siêu dự án 4100ha", "Sân Golf", "Bến du thuyền", "Kỳ quan tương lai"]
    },
    {
        "_id": "proj-4",
        "name": "Masteri West Heights",
        "slug": "masteri-west-heights",
        "location": "Tây Mỗ, Nam Từ Liêm, Hà Nội",
        "developer": "Masterise Homes",
        "shortDescription": "Căn hộ wellness cao cấp chuẩn quốc tế tọa lạc tại trung tâm đại đô thị thông minh Smart City.",
        "description": "Masteri West Heights kiến tạo một không gian sống chuẩn wellness đẳng cấp quốc tế tại trung tâm Smart City Hà Nội. Với 4 tòa căn hộ cao cấp sở hữu tầm nhìn trực diện ra hồ trung tâm 4.8ha, dự án mang lại chuỗi 22 tiện ích đặc quyền trong nhà và ngoài trời cực kỳ xa hoa.",
        "image": "https://s3-hcmc02.higiocloud.vn/intranet/logos/5a2cd415f546462a8199fb69a7725896.png",
        "banner": "https://s3-hcmc02.higiocloud.vn/intranet/logos/b38e360f491e4e99a902ea07de0cd8c0.png",
        "status": "Đang mở bán",
        "scale": "2.1 ha",
        "priceRange": "3.2 tỷ - 9.5 tỷ",
        "tags": ["Luxury Apartment", "Smart City", "Masterise Homes", "Căn hộ Wellness"]
    },
    {
        "_id": "proj-5",
        "name": "The Matrix One",
        "slug": "the-matrix-one",
        "location": "Mễ Trì, Nam Từ Liêm, Hà Nội",
        "developer": "MIK Group",
        "shortDescription": "Tổ hợp căn hộ hạng sang, biểu tượng sống mới tại trung tâm kinh tế - hành chính Mỹ Đình.",
        "description": "The Matrix One là tổ hợp căn hộ siêu sang do MIK Group phát triển. Dự án nằm tại ngã tư Lê Quang Đạo - Mễ Trì, sở hữu tầm nhìn panorama triệu đô hướng ra công viên hồ điều hòa 14ha và đường đua F1 cũ. Dự án mang tiêu chuẩn bàn giao khắt khe nhất thế giới.",
        "image": "https://s3-hcmc02.higiocloud.vn/intranet/logos/cca86fc2140141b2a287042d917a632e.png",
        "banner": "https://s3-hcmc02.higiocloud.vn/intranet/logos/62f6a55f69eb48e089fd224c353540b7.png",
        "status": "Đã bàn giao",
        "scale": "39.8 ha (toàn khu)",
        "priceRange": "5.5 tỷ - 25 tỷ",
        "tags": ["Căn hộ siêu sang", "Mỹ Đình", "MIK Group", "View công viên 14ha"]
    },
    {
        "_id": "proj-6",
        "name": "Sun Premier Village Primavera",
        "slug": "sun-primavera",
        "location": "An Thới, Phú Quốc, Kiên Giang",
        "developer": "Sun Group",
        "shortDescription": "Thị trấn Địa Trung Hải phồn hoa - Biểu tượng kiến trúc nghệ thuật và nghỉ dưỡng đẳng cấp bên bờ Nam đảo ngọc.",
        "description": "Sun Premier Village Primavera sở hữu vị trí đắc địa tại ga đi cáp treo Hòn Thơm, Phú Quốc. Dự án tái hiện một thị trấn ven biển Địa Trung Hải rực rỡ sắc màu với những căn shophouse thoải dần về phía biển, các quảng trường nghệ thuật lớn và công trình biểu tượng Cầu Hôn (Kiss Bridge).",
        "image": "https://s3-hcmc02.higiocloud.vn/intranet/logos/a2ee00e28ab046a9afa3939e8ecf170b.png",
        "banner": "https://s3-hcmc02.higiocloud.vn/intranet/logos/d192e062b72848b9993ed46a6f7b933f.png",
        "status": "Đã bàn giao",
        "scale": "39.3 ha",
        "priceRange": "18 tỷ - 85 tỷ",
        "tags": ["Địa Trung Hải", "Phú Quốc", "Sun Group", "Cận biển"]
    }
]

products = [
    {
        "_id": "prod-1",
        "title": "Biệt Thự Đơn Lập Ngọc Trai Siêu VIP - View Trực Diện Biển Hồ Ngọc Trai",
        "slug": "biet-thu-don-lap-ngoc-trai-view-bien-ho",
        "price": 95.0,
        "pricePerSqm": 317.0,
        "area": 300.0,
        "bedrooms": 5,
        "bathrooms": 6,
        "location": "Phân khu Ngọc Trai, Vinhomes Ocean Park 1",
        "description": "Siêu phẩm biệt thự đơn lập phân khu Ngọc Trai - phân khu khép kín (compound) vip nhất Vinhomes Ocean Park 1. Căn biệt thự sở hữu vị trí góc đắc địa, tầm nhìn trực diện hồ điều hòa cát trắng 24.5ha. Thiết kế kiến trúc Địa Trung Hải phóng khoáng, sang trọng với khoảng sân vườn rộng lớn bao quanh, hầm rượu và bể bơi trong nhà.",
        "projectSlug": "ocean-park-1",
        "productType": "villa",
        "productTypeName": "Biệt thự",
        "isPremium": True,
        "developer": "Vinhomes",
        "images": [
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/f38b551758ef46dd80ad140a43aa90a5.png",
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/2529cedb356b4a3384937562a13b27c7.png",
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/1c89c4098a0d4dca9b6ce80577547093.png"
        ],
        "status": "Còn hàng",
        "direction": "Đông Nam",
        "legal": "Sổ đỏ lâu dài"
    },
    {
        "_id": "prod-2",
        "title": "Biệt Thự Song Lập San Hô Kế Cận Công Viên Sóng Royal Wave Park",
        "slug": "biet-thu-song-lap-san-ho-gan-cong-vien-song",
        "price": 18.5,
        "pricePerSqm": 123.0,
        "area": 150.0,
        "bedrooms": 4,
        "bathrooms": 5,
        "location": "Phân khu San Hô, Vinhomes Ocean Park 2",
        "description": "Biệt thự song lập hoàn thiện thô phân khu San Hô tại Ocean Park 2. Vị trí vô cùng đắc địa, chỉ vài bước chân là ra tới đại công viên tạo sóng Royal Wave Park 18ha. Thiết kế phong cách Đông Dương (Indochine) độc đáo, tối ưu hóa công năng sử dụng với ban công kính rộng và cửa sổ lớn đón ánh sáng tự nhiên.",
        "projectSlug": "ocean-park-2",
        "productType": "villa",
        "productTypeName": "Biệt thự",
        "isPremium": False,
        "developer": "Vinhomes",
        "images": [
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/80c76327c91143549a64cf2b41674218.png",
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/fdac8c22ea8b4f65a2768357a5b0a5fa.png",
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/4e9da45141ed405f9894f5293b41541a.png"
        ],
        "status": "Còn hàng",
        "direction": "Nam",
        "legal": "Hợp đồng mua bán"
    },
    {
        "_id": "prod-3",
        "title": "Căn Hộ Panorama Masteri West Heights - Tòa A View Trọn Hồ Trung Tâm",
        "slug": "can-ho-panorama-masteri-west-heights-toa-a",
        "price": 4.8,
        "pricePerSqm": 69.0,
        "area": 70.0,
        "bedrooms": 2,
        "bathrooms": 2,
        "location": "Tòa A Masteri West Heights, Smart City, Hà Nội",
        "description": "Căn hộ 2 phòng ngủ 2 WC đẳng cấp tại dự án Masteri West Heights. Căn hộ ở tầng cao trung bình, sở hữu tầm nhìn trực diện và không góc chết ra hồ điều hòa trung tâm 4.8ha. Bàn giao đầy đủ thiết bị nội thất liền tường cao cấp từ các thương hiệu Kohler, Hafele, Daikin. Chủ sở hữu được tận hưởng bể bơi vô cực trên tầng thượng tòa nhà.",
        "projectSlug": "masteri-west-heights",
        "productType": "apartment",
        "productTypeName": "Căn hộ chung cư",
        "isPremium": True,
        "developer": "Masterise Homes",
        "images": [
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/fbd7dc8a8eac429e9bbca744a03a37b7.png",
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/c23c8421fbd8483fab69c37e2ddb8181.png",
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/9bf9e0d6d9f245debe70e786756e7916.png"
        ],
        "status": "Còn hàng",
        "direction": "Đông Bắc",
        "legal": "Sổ đỏ lâu dài"
    },
    {
        "_id": "prod-4",
        "title": "Căn Hộ Dual-Key Cao Cấp The Matrix One Mỹ Đình - Ban Công Panorama",
        "slug": "can-ho-dual-key-the-matrix-one-my-dinh",
        "price": 9.2,
        "pricePerSqm": 82.0,
        "area": 112.0,
        "bedrooms": 3,
        "bathrooms": 3,
        "location": "Tòa B The Matrix One, Mỹ Đình, Hà Nội",
        "description": "Căn hộ Dual-Key độc đáo tại The Matrix One, vừa thích hợp để ở vừa có thể cho thuê tạo dòng tiền ổn định. Thiết kế chia làm 2 lối đi riêng biệt dẫn vào căn studio và căn hộ 2 phòng ngủ. Toàn bộ căn hộ sử dụng kính hộp Triple Low-E chạm sàn cao cấp nhất, ngắm trọn vẹn hồ điều hòa 14ha và công viên Mỹ Đình.",
        "projectSlug": "the-matrix-one",
        "productType": "apartment",
        "productTypeName": "Căn hộ chung cư",
        "isPremium": True,
        "developer": "MIK Group",
        "images": [
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/f75cf866e6ba4deda74397da58d9fe44.png",
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/6b137d30b1744912b080e7fef0f49558.png",
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/7722a3d841a34c2e8ebe2ad2a34b6ba2.png"
        ],
        "status": "Đã cọc",
        "direction": "Tây Nam",
        "legal": "Sổ đỏ lâu dài"
    },
    {
        "_id": "prod-5",
        "title": "Nhà Phố Liền Kề Sao Biển - Vừa Ở Vừa Kinh Doanh Đắc Địa",
        "slug": "nha-pho-lien-ke-sao-bien-vinhomes-ocean-park-2",
        "price": 12.5,
        "pricePerSqm": 139.0,
        "area": 90.0,
        "bedrooms": 4,
        "bathrooms": 5,
        "location": "Phân khu Sao Biển, Vinhomes Ocean Park 2",
        "description": "Nhà phố liền kề / Shophouse phân khu Sao Biển tại Vinhomes Ocean Park 2. Trục đường giao thông chính thông thoáng, thuận tiện kinh doanh dịch vụ ăn uống, thời trang hoặc làm văn phòng đại diện. Thiết kế phong cách Pháp cổ sang trọng 5 tầng, mặt tiện 5m cực thoáng.",
        "projectSlug": "ocean-park-2",
        "productType": "townhouse",
        "productTypeName": "Nhà liền kề",
        "isPremium": False,
        "developer": "Vinhomes",
        "images": [
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/5f4b57afe5ae410caa96bf97dcd7bb56.png",
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/e368e674f46945b2a2b8686b2ca58f3c.png",
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/df4cbb38033a446d9d18d5dace3b1bc1.png"
        ],
        "status": "Còn hàng",
        "direction": "Đông Nam",
        "legal": "Sổ đỏ lâu dài"
    },
    {
        "_id": "prod-6",
        "title": "Nhà Thổ Cư 5 Tầng Phố Cổ Hà Nội - Gần Hồ Gươm, Tiện Kinh Doanh",
        "slug": "nha-tho-cu-5-tang-pho-co-ha-noi-gan-ho-guom",
        "price": 35.0,
        "pricePerSqm": 583.0,
        "area": 60.0,
        "bedrooms": 4,
        "bathrooms": 4,
        "location": "Phố Hàng Bè, Hoàn Kiếm, Hà Nội",
        "description": "Cơ hội sở hữu nhà đất thổ cư sổ đỏ chính chủ ngay trung tâm Phố Cổ Hà Nội, cách Hồ Hoàn Kiếm chỉ 3 phút đi bộ. Căn nhà thiết kế hiện đại 5 tầng chắc chắn, mặt tiền rộng 4.5m nằm tại ngõ nông ô tô đỗ cửa. Phù hợp làm homestay cao cấp cho khách nước ngoài thuê hoặc kinh doanh spa, cà phê boutique.",
        "projectSlug": "ngoai-du-an",
        "productType": "residential",
        "productTypeName": "Nhà thổ cư",
        "isPremium": False,
        "images": [
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/93274790ab734ef3b6f27851882bb574.png",
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/380fe2636f504e1e84f19ff389e21be9.png",
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/c30a89b767484cddae9e2e1d5406ea48.png"
        ],
        "status": "Còn hàng",
        "direction": "Tây",
        "legal": "Sổ đỏ lâu dài"
    },
    {
        "_id": "prod-7",
        "title": "Shophouse Địa Trung Hải Phân Khu Cát Tường - Trục Đại Lộ Hạ Long Xanh",
        "slug": "shophouse-cat-tuong-vinhomes-ha-long-xanh",
        "price": 15.0,
        "pricePerSqm": 125.0,
        "area": 120.0,
        "bedrooms": 4,
        "bathrooms": 5,
        "location": "Phân khu Cát Tường, Vinhomes Hạ Long Xanh, Quảng Ninh",
        "description": "Suất ngoại giao shophouse thương mại phân khu Cát Tường thuộc siêu dự án Vinhomes Hạ Long Xanh. Tọa lạc ngay trên mặt đại lộ kinh tế rộng 60m kết nối toàn khu. Thiết kế phong cách Địa Trung Hải rực rỡ sắc màu, lý tưởng để mở nhà hàng, cửa hàng lưu niệm hoặc văn phòng dịch vụ du lịch.",
        "projectSlug": "ha-long-xanh",
        "productType": "townhouse",
        "productTypeName": "Nhà liền kề",
        "isPremium": False,
        "developer": "Vinhomes",
        "images": [
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/66cb5c86cb7f4bf5b21957a43aac2973.png",
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/baed6456eac04207bc1640dfce21c140.png",
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/1669c1ff4dcf4a66837c6ba24ec467d2.png"
        ],
        "status": "Còn hàng",
        "direction": "Nam",
        "legal": "Hợp đồng mua bán"
    },
    {
        "_id": "prod-8",
        "title": "Dinh Thự Hoàng Gia Siêu Sang Mặt Biển Hạ Long Xanh - Kỳ Quan Giữa Lòng Kỳ Quan",
        "slug": "dinh-thu-hoang-gia-mat-bien-ha-long-xanh",
        "price": 180.0,
        "pricePerSqm": 360.0,
        "area": 500.0,
        "bedrooms": 6,
        "bathrooms": 8,
        "location": "Phân khu Vịnh Hoàng Gia, Vinhomes Hạ Long Xanh, Quảng Ninh",
        "description": "Siêu phẩm dinh thự đơn lập trực diện vịnh biển và bến du thuyền quốc tế tại Vinhomes Hạ Long Xanh. Diện tích đất 500m2 with thiết kế tân cổ điển uy nghi hoàng tráng. Sở hữu 3 mặt sân vườn giáp kênh sinh thái lớn và bãi biển riêng nhân tạo. Tiện ích bao gồm rạp chiếu phim gia đình, phòng gym, hầm rượu và bể bơi tràn bờ nước mặn.",
        "projectSlug": "ha-long-xanh",
        "productType": "villa",
        "productTypeName": "Biệt thự",
        "isPremium": True,
        "developer": "Vinhomes",
        "images": [
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/014c719c8e9b4457ad2aba1518049811.png",
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/43575aabaec24e2180c7355ec771d7cf.png",
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/2d09497a90d14707ac48cad081fc9395.png"
        ],
        "status": "Còn hàng",
        "direction": "Đông Nam",
        "legal": "Sổ đỏ lâu dài"
    },
    {
        "_id": "prod-9",
        "title": "Biệt Thự Sun Premier Village Phú Quốc - Sát Biển Bãi Khem Tuyệt Mỹ",
        "slug": "biet-thu-sun-premier-village-phu-quoc",
        "price": 65.0,
        "pricePerSqm": 217.0,
        "area": 300.0,
        "bedrooms": 4,
        "bathrooms": 5,
        "location": "Mũi Ông Đội, An Thới, Phú Quốc",
        "description": "Biệt thự nghỉ dưỡng 2 tầng sát biển tại Mũi Ông Đội, Phú Quốc. Thiết kế giật cấp độc đáo tôn vinh thiên nhiên hoang sơ, sở hữu tầm nhìn 2 mặt biển ngắm hoàng hôn và bình minh tuyệt đẹp. Tiêu chuẩn bàn giao full nội thất cao cấp 5 sao quốc tế vận hành bởi tập đoàn danh tiếng.",
        "projectSlug": "sun-primavera",
        "productType": "villa",
        "productTypeName": "Biệt thự",
        "isPremium": True,
        "developer": "Sun Group",
        "images": [
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/46bd1d49542e40e2ae578e7e7d3d1d2a.png",
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/bd780d5329cf40c2b478879abd121ff9.png",
            "https://s3-hcmc02.higiocloud.vn/intranet/logos/bdda66b49c314b8898ee6d2daba0f38b.png"
        ],
        "status": "Còn hàng",
        "direction": "Tây Nam",
        "legal": "Sổ đỏ lâu dài"
    }
]

users = [
    {
        "_id": "user-1",
        "name": "Administrator",
        "email": "hoainamtin2@gmail.com",
        "hashed_password": hash_password("admin123"),
        "role": "admin",
        "status": "active",
        "createdAt": "2026-01-15"
    },
    {
        "_id": "user-2",
        "name": "Trần Thị Nhân Viên",
        "email": "staff@realty.com",
        "hashed_password": hash_password("staff123"),
        "role": "staff",
        "status": "active",
        "createdAt": "2026-02-20"
    },
    {
        "_id": "user-3",
        "name": "Lê Văn Khóa",
        "email": "locked@realty.com",
        "hashed_password": hash_password("password123"),
        "role": "staff",
        "status": "inactive",
        "createdAt": "2026-03-10"
    }
]

posts = [
    {
        "_id": "news-1",
        "title": "Bất Động Sản Ven Biển Quảng Ninh Bứt Phá Nhờ Đòn Bẩy Hạ Tầng",
        "slug": "bat-dong-san-ven-bien-quang-ninh-but-pha-ha-tang-a8f3b",
        "summary": "Với việc hoàn thiện các tuyến cao tốc kết nối cùng dự án Hạ Long Xanh được đẩy mạnh triển khai, thị trường địa ốc Quảng Ninh đang trở thành thỏi nam châm thu hút dòng vốn đầu tư.",
        "content": "<p>Thị trường bất động sản Quảng Ninh liên tục ghi nhận những tín hiệu tích cực trong thời gian qua. Động lực chính đến từ việc hoàn thiện đồng bộ hạ tầng giao thông kết nối liên vùng như cao tốc Hà Nội - Hải Phòng - Hạ Long - Vân Đồn - Móng Cái, sân bay quốc tế Vân Đồn và cảng tàu khách quốc tế Hạ Long.</p><p>Đặc biệt, siêu dự án Vinhomes Hạ Long Xanh quy mô lớn tại trục kinh tế ven biển Quảng Yên - Hạ Long khởi công xây dựng đã thổi một luồng sinh khí mới vào toàn khu vực. Giới chuyên gia nhận định, phân khúc biệt thự nghỉ dưỡng, shophouse thương mại ven biển sẽ là điểm sáng đầu tư trung và dài hạn nhờ khai thác tối đa tiềm năng du lịch 4 mùa của địa phương.</p>",
        "image": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=600&h=400&q=80",
        "publishedAt": "2026-05-25",
        "category": "Thị trường"
    },
    {
        "_id": "news-2",
        "title": "Bí Quyết Mua Căn Hộ Chung Cư Cao Cấp Tránh Rủi Ro Pháp Lý",
        "slug": "bi-quyet-mua-can-ho-chung-cu-cao-cap-tranh-rui-ro-phap-ly-c4d2e",
        "summary": "Để không rơi vào cảnh \"tiền mất tật mang\", người mua nhà cần xem xét kỹ lưỡng hồ sơ pháp lý dự án, uy tín chủ đầu tư và các điều khoản trong hợp đồng mua bán.",
        "content": "<p>Mua chung cư cao cấp là giao dịch có giá trị lớn, đòi hỏi khách hàng phải cực kỳ tỉnh táo trước khi đặt bút ký hợp đồng. Dưới đây là những lưu ý quan trọng để đảm bảo an toàn tài chính:</p><ul><li>Kiểm tra giấy phép xây dựng, quyết định giao đất và quy hoạch chi tiết 1/500 của dự án.</li><li>Kiểm tra văn bản chấp thuận đủ điều kiện bán nhà ở hình thành trong tương lai của Sở Xây dựng sở tại.</li><li>Tìm hiểu năng lực tài chính và uy tín của chủ đầu tư thông qua các dự án đã bàn giao trước đó (ví dụ như Vinhomes, Masterise Homes với tiến độ ra sổ nhanh chóng).</li><li>Đọc kỹ chính sách bảo lãnh ngân hàng cho dự án.</li></ul>",
        "image": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=600&h=400&q=80",
        "publishedAt": "2026-05-18",
        "category": "Cẩm nang"
    },
    {
        "_id": "news-3",
        "title": "Bản Đồ Quy Hoạch Đô Thị Vệ Tinh Phía Đông Hà Nội Có Gì Mới?",
        "slug": "ban-do-quy-hoach-do-thi-ve-tinh-phia-dong-ha-noi-f2g4h",
        "summary": "Quy hoạch xây dựng thủ đô Hà Nội định hướng Gia Lâm và Văn Giang (Hưng Yên) trở thành những trung tâm đô thị sinh thái, tri thức hiện đại bậc nhất vùng thủ đô.",
        "content": "<p>Khu vực phía Đông Hà Nội đang thay đổi diện mạo nhanh chóng từng ngày. Với chiến lược \"đa cực\" trong phát triển không gian thủ đô, trục phía Đông với tâm điểm Gia Lâm và khu vực giáp ranh Văn Giang (Hưng Yên) được quy hoạch là cực tăng trưởng kinh tế mới.</p><p>Sự xuất hiện của các đại đô thị tỷ đô như Vinhomes Ocean Park 1, 2 và sắp tới là các dự án hạ tầng cầu vượt sông Hồng (cầu Trần Hưng Đạo, cầu Giang Biên) sẽ thu hút hàng chục vạn cư dân dịch chuyển từ nội đô cũ ra ngoài, biến nơi đây thành khu vực sầm uất bậc nhất phía Bắc.</p>",
        "image": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=600&h=400&q=80",
        "publishedAt": "2026-05-12",
        "category": "Quy hoạch"
    }
]

def seed_db():
    import certifi
    print(f"Connecting to database '{DB_NAME}'...")
    client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
    db = client[DB_NAME]

    # Seed Developers
    print("Seeding developers...")
    db["realty_developers"].delete_many({})
    db["realty_developers"].insert_many(developers)
    print(f"Successfully seeded {len(developers)} developers.")

    # Seed Projects
    print("Seeding projects...")
    db["realty_projects"].delete_many({})
    db["realty_projects"].insert_many(projects)
    print(f"Successfully seeded {len(projects)} projects.")

    # Seed Products
    print("Seeding products...")
    db["realty_products"].delete_many({})
    db["realty_products"].insert_many(products)
    print(f"Successfully seeded {len(products)} products.")

    # Seed Users
    print("Seeding users...")
    db["realty_users"].drop()
    db["realty_users"].create_index("email", unique=True)
    db["realty_users"].insert_many(users)
    print(f"Successfully seeded {len(users)} users.")

    # Seed Posts
    print("Seeding posts...")
    db["realty_posts"].delete_many({})
    db["realty_posts"].insert_many(posts)
    print(f"Successfully seeded {len(posts)} posts.")

    print("\nDatabase seeding completed successfully!")
    client.close()

if __name__ == "__main__":
    seed_db()
