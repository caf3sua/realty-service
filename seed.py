import os
from pymongo import MongoClient
from dotenv import load_dotenv

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
        "logo": "/images/logo-Masterise-Homes.png",
        "title": "Phong Cách Sống Hàng Hiệu",
        "description": "Nhà phát triển bất động sản hàng hiệu hàng đầu Việt Nam, hợp tác cùng các đối tác toàn cầu như Elie Saab, Marriott International. Kiến tạo giá trị sống trường tồn và dịch vụ quản lý chất lượng thế giới.",
        "slug": "masterise-homes",
        "linkText": "Xem Các Căn Hộ Masterise Homes"
    },
    {
        "_id": "dev-2",
        "name": "MIK Group",
        "logo": "/images/logo-MIK-Group.png",
        "title": "Chuẩn Mực Sống Sang Trọng",
        "description": "Nổi tiếng với định vị dòng sản phẩm hạng sang The Matrix One và Imperia, MIK Group kiến tạo các giá trị sống bền vững, thiết kế xanh hài hòa thiên nhiên kết hợp công nghệ thông minh thời thượng.",
        "slug": "mik-group",
        "linkText": "Xem Các Căn Hộ MIK Group"
    },
    {
        "_id": "dev-3",
        "name": "Vinhomes",
        "logo": "/images/logo-vinhomes.png",
        "title": "Đại Đô Thị Biển Quốc Tế",
        "description": "Thương hiệu bất động sản số 1 Việt Nam, nổi bật với các siêu dự án đô thị sinh thái kết hợp biển hồ nhân tạo kỳ vĩ, quy hoạch đồng bộ \"Tất cả trong một\" kiến tạo chuẩn mực sống văn minh hiện đại hàng đầu.",
        "slug": "vinhomes",
        "linkText": "Xem Các Sản Phẩm Vinhomes"
    },
    {
        "_id": "dev-4",
        "name": "Sun Group",
        "logo": "/images/logo-sun-group.png",
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
        "image": "/images/project-op1.png",
        "banner": "/images/project-op1-banner.png",
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
        "image": "/images/project-op2.png",
        "banner": "/images/project-op2-banner.png",
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
        "image": "/images/project-hlx.png",
        "banner": "/images/project-hlx-banner.png",
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
        "image": "/images/project-masteri.png",
        "banner": "/images/project-masteri-banner.png",
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
        "image": "/images/project-mik.png",
        "banner": "/images/project-mik-banner.png",
        "status": "Đã bàn giao",
        "scale": "39.8 ha (toàn khu)",
        "priceRange": "5.5 tỷ - 25 tỷ",
        "tags": ["Căn hộ siêu sang", "Mỹ Đình", 'MIK Group', 'View công viên 14ha']
    },
    {
        "_id": "proj-6",
        "name": "Sun Premier Village Primavera",
        "slug": "sun-primavera",
        "location": "An Thới, Phú Quốc, Kiên Giang",
        "developer": "Sun Group",
        "shortDescription": "Thị trấn Địa Trung Hải phồn hoa - Biểu tượng kiến trúc nghệ thuật và nghỉ dưỡng đẳng cấp bên bờ Nam đảo ngọc.",
        "description": "Sun Premier Village Primavera sở hữu vị trí đắc địa tại ga đi cáp treo Hòn Thơm, Phú Quốc. Dự án tái hiện một thị trấn ven biển Địa Trung Hải rực rỡ sắc màu với những căn shophouse thoải dần về phía biển, các quảng trường nghệ thuật lớn và công trình biểu tượng Cầu Hôn (Kiss Bridge).",
        "image": "/images/project-sun.png",
        "banner": "/images/project-sun.png",
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
        "pricePerSqm": 316.6,
        "area": 300,
        "bedrooms": 5,
        "bathrooms": 6,
        "location": "Phân khu Ngọc Trai, Vinhomes Ocean Park 1",
        "description": "Siêu phẩm biệt thự đơn lập phân khu Ngọc Trai - phân khu khép kín (compound) vip nhất Vinhomes Ocean Park 1. Căn biệt thự sở hữu vị trí góc đắc địa, tầm nhìn trực diện hồ điều hòa cát trắng 24.5ha. Thiết kế kiến trúc Địa Trung Hải phóng khoáng, sang trọng với khoảng sân vườn rộng lớn bao quanh, hầm rượu và bể bơi trong nhà.",
        "projectSlug": "ocean-park-1",
        "productType": "villa",
        "productTypeName": "Biệt thự",
        "isPremium": True,
        "developer": "Vinhomes",
        "images": ["/images/prop-villa-1.png", "/images/prop-villa-1-int.png", "/images/prop-villa-1-ext2.png"],
        "status": "Còn hàng",
        "direction": "Đông Nam",
        "legal": "Sổ đỏ lâu dài"
    },
    {
        "_id": "prod-2",
        "title": "Biệt Thự Song Lập San Hô Kế Cận Công Viên Sóng Royal Wave Park",
        "slug": "biet-thu-song-lap-san-ho-gan-cong-vien-song",
        "price": 18.5,
        "pricePerSqm": 123.3,
        "area": 150,
        "bedrooms": 4,
        "bathrooms": 5,
        "location": "Phân khu San Hô, Vinhomes Ocean Park 2",
        "description": "Biệt thự song lập hoàn thiện thô phân khu San Hô tại Ocean Park 2. Vị trí vô cùng đắc địa, chỉ vài bước chân là ra tới đại công viên tạo sóng Royal Wave Park 18ha. Thiết kế phong cách Đông Dương (Indochine) độc đáo, tối ưu hóa công năng sử dụng với ban công kính rộng và cửa sổ lớn đón ánh sáng tự nhiên.",
        "projectSlug": "ocean-park-2",
        "productType": "villa",
        "productTypeName": "Biệt thự",
        "isPremium": False,
        "developer": "Vinhomes",
        "images": ["/images/prop-villa-2.png", "/images/prop-villa-2-int.png", "/images/prop-villa-2-ext2.png"],
        "status": "Còn hàng",
        "direction": "Nam",
        "legal": "Hợp đồng mua bán"
    },
    {
        "_id": "prod-3",
        "title": "Căn Hộ Panorama Masteri West Heights - Tòa A View Trọn Hồ Trung Tâm",
        "slug": "can-ho-panorama-masteri-west-heights-toa-a",
        "price": 4.8,
        "pricePerSqm": 68.5,
        "area": 70,
        "bedrooms": 2,
        "bathrooms": 2,
        "location": "Tòa A Masteri West Heights, Smart City, Hà Nội",
        "description": "Căn hộ 2 phòng ngủ 2 WC đẳng cấp tại dự án Masteri West Heights. Căn hộ ở tầng cao trung bình, sở hữu tầm nhìn trực diện và không góc chết ra hồ điều hòa trung tâm 4.8ha. Bàn giao đầy đủ thiết bị nội thất liền tường cao cấp từ các thương hiệu Kohler, Hafele, Daikin. Chủ sở hữu được tận hưởng bể bơi vô cực trên tầng thượng tòa nhà.",
        "projectSlug": "masteri-west-heights",
        "productType": "apartment",
        "productTypeName": "Căn hộ",
        "isPremium": True,
        "developer": "Masterise Homes",
        "images": ["/images/prop-apartment-1.png", "/images/prop-apartment-1-int.png", "/images/prop-apartment-1-ext2.png"],
        "status": "Còn hàng",
        "direction": "Đông Bắc",
        "legal": "Sổ đỏ lâu dài"
    },
    {
        "_id": "prod-4",
        "title": "Căn Hộ Dual-Key Cao Cấp The Matrix One Mỹ Đình - Ban Công Panorama",
        "slug": "can-ho-dual-key-the-matrix-one-my-dinh",
        "price": 9.2,
        "pricePerSqm": 82.1,
        "area": 112,
        "bedrooms": 3,
        "bathrooms": 3,
        "location": "Tòa B The Matrix One, Mỹ Đình, Hà Nội",
        "description": "Căn hộ Dual-Key độc đáo tại The Matrix One, vừa thích hợp để ở vừa có thể cho thuê tạo dòng tiền ổn định. Thiết kế chia làm 2 lối đi riêng biệt dẫn vào căn studio và căn hộ 2 phòng ngủ. Toàn bộ căn hộ sử dụng kính hộp Triple Low-E chạm sàn cao cấp nhất, ngắm trọn vẹn hồ điều hòa 14ha và công viên Mỹ Đình.",
        "projectSlug": "the-matrix-one",
        "productType": "apartment",
        "productTypeName": "Căn hộ",
        "isPremium": True,
        "developer": "MIK Group",
        "images": ["/images/prop-apartment-2.png", "/images/prop-apartment-2-int.png", "/images/prop-apartment-2-ext2.png"],
        "status": "Đã cọc",
        "direction": "Tây Nam",
        "legal": "Sổ đỏ lâu dài"
    },
    {
        "_id": "prod-5",
        "title": "Nhà Phố Liền Kề Sao Biển - Vừa Ở Vừa Kinh Doanh Đắc Địa",
        "slug": "nha-pho-lien-ke-sao-bien-vinhomes-ocean-park-2",
        "price": 12.5,
        "pricePerSqm": 138.8,
        "area": 90,
        "bedrooms": 4,
        "bathrooms": 5,
        "location": "Phân khu Sao Biển, Vinhomes Ocean Park 2",
        "description": "Nhà phố liền kề / Shophouse phân khu Sao Biển tại Vinhomes Ocean Park 2. Trục đường giao thông chính thông thoáng, thuận tiện kinh doanh dịch vụ ăn uống, thời trang hoặc làm văn phòng đại diện. Thiết kế phong cách Pháp cổ sang trọng 5 tầng, mặt tiền 5m cực thoáng.",
        "projectSlug": "ocean-park-2",
        "productType": "townhouse",
        "productTypeName": "Liền kề",
        "isPremium": False,
        "developer": "Vinhomes",
        "images": ["/images/prop-townhouse-1.png", "/images/prop-townhouse-1-int.png", "/images/prop-townhouse-1-ext2.png"],
        "status": "Còn hàng",
        "direction": "Đông Nam",
        "legal": "Sổ đỏ lâu dài"
    },
    {
        "_id": "prod-6",
        "title": "Nhà Thổ Cư 5 Tầng Phố Cổ Hà Nội - Gần Hồ Gươm, Tiện Kinh Doanh",
        "slug": "nha-tho-cu-5-tang-pho-co-ha-noi-gan-ho-guom",
        "price": 35.0,
        "pricePerSqm": 583.3,
        "area": 60,
        "bedrooms": 4,
        "bathrooms": 4,
        "location": "Phố Hàng Bè, Hoàn Kiếm, Hà Nội",
        "description": "Cơ hội sở hữu nhà đất thổ cư sổ đỏ chính chủ ngay trung tâm Phố Cổ Hà Nội, cách Hồ Hoàn Kiếm chỉ 3 phút đi bộ. Căn nhà thiết kế hiện đại 5 tầng chắc chắn, mặt tiền rộng 4.5m nằm tại ngõ nông ô tô đỗ cửa. Phù hợp làm homestay cao cấp cho khách nước ngoài thuê hoặc kinh doanh spa, cà phê boutique.",
        "projectSlug": "ngoai-du-an",
        "productType": "residential",
        "productTypeName": "Nhà thổ cư",
        "isPremium": False,
        "images": ["/images/prop-townhouse-2.png", "/images/prop-townhouse-2-int.png", "/images/prop-townhouse-2-ext2.png"],
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
        "area": 120,
        "bedrooms": 4,
        "bathrooms": 5,
        "location": "Phân khu Cát Tường, Vinhomes Hạ Long Xanh, Quảng Ninh",
        "description": "Suất ngoại giao shophouse thương mại phân khu Cát Tường thuộc siêu dự án Vinhomes Hạ Long Xanh. Tọa lạc ngay trên mặt đại lộ kinh tế rộng 60m kết nối toàn khu. Thiết kế phong cách Địa Trung Hải rực rỡ sắc màu, lý tưởng để mở nhà hàng, cửa hàng lưu niệm hoặc văn phòng dịch vụ du lịch.",
        "projectSlug": "ha-long-xanh",
        "productType": "townhouse",
        "productTypeName": "Liền kề",
        "isPremium": False,
        "developer": "Vinhomes",
        "images": ["/images/prop-townhouse-1.png", "/images/prop-townhouse-1-int.png", "/images/prop-townhouse-1-ext2.png"],
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
        "area": 500,
        "bedrooms": 6,
        "bathrooms": 8,
        "location": "Phân khu Vịnh Hoàng Gia, Vinhomes Hạ Long Xanh, Quảng Ninh",
        "description": "Siêu phẩm dinh thự đơn lập trực diện vịnh biển và bến du thuyền quốc tế tại Vinhomes Hạ Long Xanh. Diện tích đất 500m2 with thiết kế tân cổ điển uy nghi hoàng tráng. Sở hữu 3 mặt sân vườn giáp kênh sinh thái lớn và bãi biển riêng nhân tạo. Tiện ích bao gồm rạp chiếu phim gia đình, phòng gym, hầm rượu và bể bơi tràn bờ nước mặn.",
        "projectSlug": "ha-long-xanh",
        "productType": "villa",
        "productTypeName": "Biệt thự",
        "isPremium": True,
        "developer": "Vinhomes",
        "images": ["/images/ha-long-xanh-hero.png", "/images/prop-villa-1-int.png", "/images/prop-villa-1-ext2.png"],
        "status": "Còn hàng",
        "direction": "Đông Nam",
        "legal": "Sổ đỏ lâu dài"
    },
    {
        "_id": "prod-9",
        "title": "Biệt Thự Sun Premier Village Phú Quốc - Sát Biển Bãi Khem Tuyệt Mỹ",
        "slug": "biet-thu-sun-premier-village-phu-quoc",
        "price": 65.0,
        "pricePerSqm": 216.6,
        "area": 300,
        "bedrooms": 4,
        "bathrooms": 5,
        "location": "Mũi Ông Đội, An Thới, Phú Quốc",
        "description": "Biệt thự nghỉ dưỡng 2 tầng sát biển tại Mũi Ông Đội, Phú Quốc. Thiết kế giật cấp độc đáo tôn vinh thiên nhiên hoang sơ, sở hữu tầm nhìn 2 mặt biển ngắm hoàng hôn và bình minh tuyệt đẹp. Tiêu chuẩn bàn giao full nội thất cao cấp 5 sao quốc tế vận hành bởi tập đoàn danh tiếng.",
        "projectSlug": "sun-primavera",
        "productType": "villa",
        "productTypeName": "Biệt thự",
        "isPremium": True,
        "developer": "Sun Group",
        "images": ["/images/prop-villa-sun.png", "/images/prop-villa-sun-int.png", "/images/prop-villa-sun-ext2.png"],
        "status": "Còn hàng",
        "direction": "Tây Nam",
        "legal": "Sổ đỏ lâu dài"
    }
]

def seed_db():
    print(f"Connecting to database '{DB_NAME}'...")
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]

    # Seed Developers
    print("Seeding developers...")
    db["developers"].delete_many({})
    db["developers"].insert_many(developers)
    print(f"Successfully seeded {len(developers)} developers.")

    # Seed Projects
    print("Seeding projects...")
    db["projects"].delete_many({})
    db["projects"].insert_many(projects)
    print(f"Successfully seeded {len(projects)} projects.")

    # Seed Products
    print("Seeding products...")
    db["products"].delete_many({})
    db["products"].insert_many(products)
    print(f"Successfully seeded {len(products)} products.")

    print("\nDatabase seeding completed successfully!")
    client.close()

if __name__ == "__main__":
    seed_db()
