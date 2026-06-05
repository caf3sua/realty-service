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
developers = [   {   '_id': 'dev-1',
        'description': 'Nhà phát triển bất động sản hàng hiệu hàng đầu Việt Nam, hợp tác cùng các đối tác toàn cầu như '
                       'Elie Saab, Marriott International. Kiến tạo giá trị sống trường tồn và dịch vụ quản lý chất '
                       'lượng thế giới.',
        'linkText': 'Xem Các Căn Hộ Masterise Homes',
        'logo': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/0aabde5297104d3fb5988d5962f4106e.png',
        'name': 'Masterise Homes',
        'slug': 'masterise-homes',
        'title': 'Phong Cách Sống Hàng Hiệu'},
    {   '_id': 'dev-2',
        'description': 'Nổi tiếng với định vị dòng sản phẩm hạng sang The Matrix One và Imperia, MIK Group kiến tạo '
                       'các giá trị sống bền vững, thiết kế xanh hài hòa thiên nhiên kết hợp công nghệ thông minh thời '
                       'thượng.',
        'linkText': 'Xem Các Căn Hộ MIK Group',
        'logo': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/1078c53f86aa4101adba8ebb6cf5ae80.png',
        'name': 'MIK Group',
        'slug': 'mik-group',
        'title': 'Chuẩn Mực Sống Sang Trọng'},
    {   '_id': 'dev-3',
        'description': 'Thương hiệu bất động sản số 1 Việt Nam, nổi bật với các siêu dự án đô thị sinh thái kết hợp '
                       'biển hồ nhân tạo kỳ vĩ, quy hoạch đồng bộ "Tất cả trong một" kiến tạo chuẩn mực sống văn minh '
                       'hiện đại hàng đầu.',
        'linkText': 'Xem Các Sản Phẩm Vinhomes',
        'logo': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/814d34d8c44d417494d5eacd8bfda06c.png',
        'name': 'Vinhomes',
        'slug': 'vinhomes',
        'title': 'Đại Đô Thị Biển Quốc Tế'},
    {   '_id': 'dev-4',
        'description': 'Tập đoàn hàng đầu trong phát triển bất động sản gắn liền với du lịch nghỉ dưỡng cao cấp, '
                       'shophouse phong cách nghệ thuật Địa Trung Hải và các dinh thiện biển tráng lệ hòa mình cùng '
                       'thiên nhiên kỳ vĩ.',
        'linkText': 'Xem Các Sản Phẩm Sun Group',
        'logo': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/804933c49a964efe815b86b12d6ef9da.png',
        'name': 'Sun Group',
        'slug': 'sun-group',
        'title': 'Kiệt Tác Nghỉ Dưỡng Độc Bản'}]

projects = [   {   '_id': 'proj-1',
        'banner': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/a9319aca6c8e44168ba033da3ea78419.png',
        'description': 'Vinhomes Ocean Park 1 sở hữu đại tiện ích độc đáo gồm Biển hồ nước mặn 6,1ha và Hồ Ngọc Trai '
                       'cát trắng 24,5ha. Dự án được quy hoạch đồng bộ mang tầm cỡ quốc tế, cung cấp đa dạng dòng sản '
                       'phẩm từ căn hộ chung cư cao cấp đến các căn biệt thự, liền kề, shophouse đẳng cấp.',
        'developer': 'Vinhomes',
        'image': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/a0bbaaf456e241018de94bfdac6f5801.png',
        'location': 'Gia Lâm, Hà Nội',
        'name': 'Vinhomes Ocean Park 1',
        'priceRange': '2.5 tỷ - 120 tỷ',
        'scale': '420 ha',
        'shortDescription': 'Thành phố Biển hồ - Nơi mang biển xanh cát trắng vào lòng Hà Nội với hồ nước mặn nhân tạo '
                            'rộng lớn.',
        'slug': 'ocean-park-1',
        'status': 'Đã bàn giao',
        'tags': ['Biển hồ nhân tạo', 'Hồ nước ngọt lớn', 'Gia Lâm', 'Vinhomes']},
    {   '_id': 'proj-2',
        'banner': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/98645964f3d845d994b72096a0f37af8.png',
        'description': 'Vinhomes Ocean Park 2 (The Empire) là giai đoạn 2 của siêu quần thể đô thị biển Vinhomes, nổi '
                       'bật với Tổ hợp công viên Biển tạo sóng nhân tạo Royal Wave Park lớn nhất thế giới (18ha). Dự '
                       'án bao gồm các phân khu mang phong cách kiến trúc đa dạng từ Pháp, Ý, Địa Trung Hải đến Đông '
                       'Dương.',
        'developer': 'Vinhomes',
        'image': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/a8c4310ea0cc4c808edf7bcd0ef436cd.png',
        'location': 'Văn Giang, Hưng Yên',
        'name': 'Vinhomes Ocean Park 2',
        'priceRange': '6 tỷ - 150 tỷ',
        'scale': '458 ha',
        'shortDescription': 'Kinh đô Ánh sáng - Siêu quần thể đô thị biển quy mô 1.000 ha với công viên sóng Royal '
                            'Wave Park quy mô nhất.',
        'slug': 'ocean-park-2',
        'status': 'Đang mở bán',
        'tags': ['Công viên sóng', 'Kinh đô ánh sáng', 'Biệt thự tân cổ điển', 'Vinhomes']},
    {   '_id': 'proj-3',
        'banner': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/aa3fb90a60004e9fb4f5d45f13cec943.png',
        'description': 'Vinhomes Hạ Long Xanh là siêu dự án phức hợp mang tính biểu tượng tại Quảng Ninh. Tọa lạc tại '
                       'vị trí vàng kết nối trực tiếp cao tốc Hải Phòng - Hạ Long, dự án tích hợp hệ sinh thái nghỉ '
                       'dưỡng, sân golf 18 lỗ, công viên chủ đề Safari, bến du thuyền quốc tế và các khu đô thị sinh '
                       'thái hiện đại bậc nhất châu Á.',
        'developer': 'Vinhomes',
        'image': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/d97a42ce702747d4accfe16f57efbb68.png',
        'location': 'Quảng Yên & Hạ Long, Quảng Ninh',
        'name': 'Vinhomes Hạ Long Xanh',
        'priceRange': 'Liên hệ',
        'scale': '4.109 ha',
        'shortDescription': 'Đại đô thị sinh thái thông minh, vịnh biển kỳ quan của tương lai với quy mô hơn 4.100 ha.',
        'slug': 'ha-long-xanh',
        'status': 'Sắp mở bán',
        'tags': ['Siêu dự án 4100ha', 'Sân Golf', 'Bến du thuyền', 'Kỳ quan tương lai']},
    {   '_id': 'proj-4',
        'banner': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/b38e360f491e4e99a902ea07de0cd8c0.png',
        'description': 'Masteri West Heights kiến tạo một không gian sống chuẩn wellness đẳng cấp quốc tế tại trung '
                       'tâm Smart City Hà Nội. Với 4 tòa căn hộ cao cấp sở hữu tầm nhìn trực diện ra hồ trung tâm '
                       '4.8ha, dự án mang lại chuỗi 22 tiện ích đặc quyền trong nhà và ngoài trời cực kỳ xa hoa.',
        'developer': 'Masterise Homes',
        'image': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/5a2cd415f546462a8199fb69a7725896.png',
        'location': 'Tây Mỗ, Nam Từ Liêm, Hà Nội',
        'name': 'Masteri West Heights',
        'priceRange': '3.2 tỷ - 9.5 tỷ',
        'scale': '2.1 ha',
        'shortDescription': 'Căn hộ wellness cao cấp chuẩn quốc tế tọa lạc tại trung tâm đại đô thị thông minh Smart '
                            'City.',
        'slug': 'masteri-west-heights',
        'status': 'Đang mở bán',
        'tags': ['Luxury Apartment', 'Smart City', 'Masterise Homes', 'Căn hộ Wellness']},
    {   '_id': 'proj-5',
        'banner': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/62f6a55f69eb48e089fd224c353540b7.png',
        'description': 'The Matrix One là tổ hợp căn hộ siêu sang do MIK Group phát triển. Dự án nằm tại ngã tư Lê '
                       'Quang Đạo - Mễ Trì, sở hữu tầm nhìn panorama triệu đô hướng ra công viên hồ điều hòa 14ha và '
                       'đường đua F1 cũ. Dự án mang tiêu chuẩn bàn giao khắt khe nhất thế giới.',
        'developer': 'MIK Group',
        'image': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/cca86fc2140141b2a287042d917a632e.png',
        'location': 'Mễ Trì, Nam Từ Liêm, Hà Nội',
        'name': 'The Matrix One',
        'priceRange': '5.5 tỷ - 25 tỷ',
        'scale': '39.8 ha (toàn khu)',
        'shortDescription': 'Tổ hợp căn hộ hạng sang, biểu tượng sống mới tại trung tâm kinh tế - hành chính Mỹ Đình.',
        'slug': 'the-matrix-one',
        'status': 'Đã bàn giao',
        'tags': ['Căn hộ siêu sang', 'Mỹ Đình', 'MIK Group', 'View công viên 14ha']},
    {   '_id': 'proj-6',
        'banner': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/d192e062b72848b9993ed46a6f7b933f.png',
        'description': 'Sun Premier Village Primavera sở hữu vị trí đắc địa tại ga đi cáp treo Hòn Thơm, Phú Quốc. Dự '
                       'án tái hiện một thị trấn ven biển Địa Trung Hải rực rỡ sắc màu với những căn shophouse thoải '
                       'dần về phía biển, các quảng trường nghệ thuật lớn và công trình biểu tượng Cầu Hôn (Kiss '
                       'Bridge).',
        'developer': 'Sun Group',
        'image': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/a2ee00e28ab046a9afa3939e8ecf170b.png',
        'location': 'An Thới, Phú Quốc, Kiên Giang',
        'name': 'Sun Premier Village Primavera',
        'priceRange': '18 tỷ - 85 tỷ',
        'scale': '39.3 ha',
        'shortDescription': 'Thị trấn Địa Trung Hải phồn hoa - Biểu tượng kiến trúc nghệ thuật và nghỉ dưỡng đẳng cấp '
                            'bên bờ Nam đảo ngọc.',
        'slug': 'sun-primavera',
        'status': 'Đã bàn giao',
        'tags': ['Địa Trung Hải', 'Phú Quốc', 'Sun Group', 'Cận biển']}]

products = [   {   '_id': 'prod-1',
        'area': 300.0,
        'bathrooms': 6,
        'bedrooms': 5,
        'description': 'Siêu phẩm biệt thự đơn lập phân khu Ngọc Trai - phân khu khép kín (compound) vip nhất Vinhomes '
                       'Ocean Park 1. Căn biệt thự sở hữu vị trí góc đắc địa, tầm nhìn trực diện hồ điều hòa cát trắng '
                       '24.5ha. Thiết kế kiến trúc Địa Trung Hải phóng khoáng, sang trọng với khoảng sân vườn rộng lớn '
                       'bao quanh, hầm rượu và bể bơi trong nhà.',
        'developer': 'Vinhomes',
        'direction': 'Đông Nam',
        'images': [   'https://s3-hcmc02.higiocloud.vn/intranet/logos/f38b551758ef46dd80ad140a43aa90a5.png',
                      'https://s3-hcmc02.higiocloud.vn/intranet/logos/2529cedb356b4a3384937562a13b27c7.png',
                      'https://s3-hcmc02.higiocloud.vn/intranet/logos/1c89c4098a0d4dca9b6ce80577547093.png'],
        'isPremium': True,
        'legal': 'Sổ đỏ lâu dài',
        'location': 'Phân khu Ngọc Trai, Vinhomes Ocean Park 1',
        'price': 95.0,
        'pricePerSqm': 317.0,
        'productType': 'villa',
        'productTypeName': 'Biệt thự',
        'projectSlug': 'ocean-park-1',
        'slug': 'biet-thu-don-lap-ngoc-trai-view-bien-ho',
        'status': 'Còn hàng',
        'title': 'Biệt Thự Đơn Lập Ngọc Trai Siêu VIP - View Trực Diện Biển Hồ Ngọc Trai'},
    {   '_id': 'prod-2',
        'area': 150.0,
        'bathrooms': 5,
        'bedrooms': 4,
        'description': 'Biệt thự song lập hoàn thiện thô phân khu San Hô tại Ocean Park 2. Vị trí vô cùng đắc địa, chỉ '
                       'vài bước chân là ra tới đại công viên tạo sóng Royal Wave Park 18ha. Thiết kế phong cách Đông '
                       'Dương (Indochine) độc đáo, tối ưu hóa công năng sử dụng với ban công kính rộng và cửa sổ lớn '
                       'đón ánh sáng tự nhiên.',
        'developer': 'Vinhomes',
        'direction': 'Nam',
        'images': [   'https://s3-hcmc02.higiocloud.vn/intranet/logos/80c76327c91143549a64cf2b41674218.png',
                      'https://s3-hcmc02.higiocloud.vn/intranet/logos/fdac8c22ea8b4f65a2768357a5b0a5fa.png',
                      'https://s3-hcmc02.higiocloud.vn/intranet/logos/4e9da45141ed405f9894f5293b41541a.png'],
        'isPremium': False,
        'legal': 'Hợp đồng mua bán',
        'location': 'Phân khu San Hô, Vinhomes Ocean Park 2',
        'price': 18.5,
        'pricePerSqm': 123.0,
        'productType': 'villa',
        'productTypeName': 'Biệt thự',
        'projectSlug': 'ocean-park-2',
        'slug': 'biet-thu-song-lap-san-ho-gan-cong-vien-song',
        'status': 'Còn hàng',
        'title': 'Biệt Thự Song Lập San Hô Kế Cận Công Viên Sóng Royal Wave Park'},
    {   '_id': 'prod-3',
        'area': 70.0,
        'bathrooms': 2,
        'bedrooms': 2,
        'description': 'Căn hộ 2 phòng ngủ 2 WC đẳng cấp tại dự án Masteri West Heights. Căn hộ ở tầng cao trung bình, '
                       'sở hữu tầm nhìn trực diện và không góc chết ra hồ điều hòa trung tâm 4.8ha. Bàn giao đầy đủ '
                       'thiết bị nội thất liền tường cao cấp từ các thương hiệu Kohler, Hafele, Daikin. Chủ sở hữu '
                       'được tận hưởng bể bơi vô cực trên tầng thượng tòa nhà.',
        'developer': 'Masterise Homes',
        'direction': 'Đông Bắc',
        'images': [   'https://s3-hcmc02.higiocloud.vn/intranet/logos/fbd7dc8a8eac429e9bbca744a03a37b7.png',
                      'https://s3-hcmc02.higiocloud.vn/intranet/logos/c23c8421fbd8483fab69c37e2ddb8181.png',
                      'https://s3-hcmc02.higiocloud.vn/intranet/logos/9bf9e0d6d9f245debe70e786756e7916.png'],
        'isPremium': True,
        'legal': 'Sổ đỏ lâu dài',
        'location': 'Tòa A Masteri West Heights, Smart City, Hà Nội',
        'price': 4.8,
        'pricePerSqm': 69.0,
        'productType': 'apartment',
        'productTypeName': 'Căn hộ chung cư',
        'projectSlug': 'masteri-west-heights',
        'slug': 'can-ho-panorama-masteri-west-heights-toa-a',
        'status': 'Còn hàng',
        'title': 'Căn Hộ Panorama Masteri West Heights - Tòa A View Trọn Hồ Trung Tâm'},
    {   '_id': 'prod-4',
        'area': 112.0,
        'bathrooms': 3,
        'bedrooms': 3,
        'description': 'Căn hộ Dual-Key độc đáo tại The Matrix One, vừa thích hợp để ở vừa có thể cho thuê tạo dòng '
                       'tiền ổn định. Thiết kế chia làm 2 lối đi riêng biệt dẫn vào căn studio và căn hộ 2 phòng ngủ. '
                       'Toàn bộ căn hộ sử dụng kính hộp Triple Low-E chạm sàn cao cấp nhất, ngắm trọn vẹn hồ điều hòa '
                       '14ha và công viên Mỹ Đình.',
        'developer': 'MIK Group',
        'direction': 'Tây Nam',
        'images': [   'https://s3-hcmc02.higiocloud.vn/intranet/logos/f75cf866e6ba4deda74397da58d9fe44.png',
                      'https://s3-hcmc02.higiocloud.vn/intranet/logos/6b137d30b1744912b080e7fef0f49558.png',
                      'https://s3-hcmc02.higiocloud.vn/intranet/logos/7722a3d841a34c2e8ebe2ad2a34b6ba2.png'],
        'isPremium': True,
        'legal': 'Sổ đỏ lâu dài',
        'location': 'Tòa B The Matrix One, Mỹ Đình, Hà Nội',
        'price': 9.2,
        'pricePerSqm': 82.0,
        'productType': 'apartment',
        'productTypeName': 'Căn hộ chung cư',
        'projectSlug': 'the-matrix-one',
        'slug': 'can-ho-dual-key-the-matrix-one-my-dinh',
        'status': 'Đã cọc',
        'title': 'Căn Hộ Dual-Key Cao Cấp The Matrix One Mỹ Đình - Ban Công Panorama'},
    {   '_id': 'prod-5',
        'area': 90.0,
        'bathrooms': 5,
        'bedrooms': 4,
        'description': 'Nhà phố liền kề / Shophouse phân khu Sao Biển tại Vinhomes Ocean Park 2. Trục đường giao thông '
                       'chính thông thoáng, thuận tiện kinh doanh dịch vụ ăn uống, thời trang hoặc làm văn phòng đại '
                       'diện. Thiết kế phong cách Pháp cổ sang trọng 5 tầng, mặt tiện 5m cực thoáng.',
        'developer': 'Vinhomes',
        'direction': 'Đông Nam',
        'images': [   'https://s3-hcmc02.higiocloud.vn/intranet/logos/5f4b57afe5ae410caa96bf97dcd7bb56.png',
                      'https://s3-hcmc02.higiocloud.vn/intranet/logos/e368e674f46945b2a2b8686b2ca58f3c.png',
                      'https://s3-hcmc02.higiocloud.vn/intranet/logos/df4cbb38033a446d9d18d5dace3b1bc1.png'],
        'isPremium': False,
        'legal': 'Sổ đỏ lâu dài',
        'location': 'Phân khu Sao Biển, Vinhomes Ocean Park 2',
        'price': 12.5,
        'pricePerSqm': 139.0,
        'productType': 'townhouse',
        'productTypeName': 'Nhà liền kề',
        'projectSlug': 'ocean-park-2',
        'slug': 'nha-pho-lien-ke-sao-bien-vinhomes-ocean-park-2',
        'status': 'Còn hàng',
        'title': 'Nhà Phố Liền Kề Sao Biển - Vừa Ở Vừa Kinh Doanh Đắc Địa'},
    {   '_id': 'prod-6',
        'area': 60.0,
        'bathrooms': 4,
        'bedrooms': 4,
        'description': 'Cơ hội sở hữu nhà đất thổ cư sổ đỏ chính chủ ngay trung tâm Phố Cổ Hà Nội, cách Hồ Hoàn Kiếm '
                       'chỉ 3 phút đi bộ. Căn nhà thiết kế hiện đại 5 tầng chắc chắn, mặt tiền rộng 4.5m nằm tại ngõ '
                       'nông ô tô đỗ cửa. Phù hợp làm homestay cao cấp cho khách nước ngoài thuê hoặc kinh doanh spa, '
                       'cà phê boutique.',
        'direction': 'Tây',
        'images': [   'https://s3-hcmc02.higiocloud.vn/intranet/logos/93274790ab734ef3b6f27851882bb574.png',
                      'https://s3-hcmc02.higiocloud.vn/intranet/logos/380fe2636f504e1e84f19ff389e21be9.png',
                      'https://s3-hcmc02.higiocloud.vn/intranet/logos/c30a89b767484cddae9e2e1d5406ea48.png'],
        'isPremium': False,
        'legal': 'Sổ đỏ lâu dài',
        'location': 'Phố Hàng Bè, Hoàn Kiếm, Hà Nội',
        'price': 35.0,
        'pricePerSqm': 583.0,
        'productType': 'residential',
        'productTypeName': 'Nhà thổ cư',
        'projectSlug': 'ngoai-du-an',
        'slug': 'nha-tho-cu-5-tang-pho-co-ha-noi-gan-ho-guom',
        'status': 'Còn hàng',
        'title': 'Nhà Thổ Cư 5 Tầng Phố Cổ Hà Nội - Gần Hồ Gươm, Tiện Kinh Doanh'},
    {   '_id': 'prod-7',
        'area': 120.0,
        'bathrooms': 5,
        'bedrooms': 4,
        'description': 'Suất ngoại giao shophouse thương mại phân khu Cát Tường thuộc siêu dự án Vinhomes Hạ Long '
                       'Xanh. Tọa lạc ngay trên mặt đại lộ kinh tế rộng 60m kết nối toàn khu. Thiết kế phong cách Địa '
                       'Trung Hải rực rỡ sắc màu, lý tưởng để mở nhà hàng, cửa hàng lưu niệm hoặc văn phòng dịch vụ du '
                       'lịch.',
        'developer': 'Vinhomes',
        'direction': 'Nam',
        'images': [   'https://s3-hcmc02.higiocloud.vn/intranet/logos/66cb5c86cb7f4bf5b21957a43aac2973.png',
                      'https://s3-hcmc02.higiocloud.vn/intranet/logos/baed6456eac04207bc1640dfce21c140.png',
                      'https://s3-hcmc02.higiocloud.vn/intranet/logos/1669c1ff4dcf4a66837c6ba24ec467d2.png'],
        'isPremium': False,
        'legal': 'Hợp đồng mua bán',
        'location': 'Phân khu Cát Tường, Vinhomes Hạ Long Xanh, Quảng Ninh',
        'price': 15.0,
        'pricePerSqm': 125.0,
        'productType': 'townhouse',
        'productTypeName': 'Nhà liền kề',
        'projectSlug': 'ha-long-xanh',
        'slug': 'shophouse-cat-tuong-vinhomes-ha-long-xanh',
        'status': 'Còn hàng',
        'title': 'Shophouse Địa Trung Hải Phân Khu Cát Tường - Trục Đại Lộ Hạ Long Xanh'},
    {   '_id': 'prod-8',
        'area': 500.0,
        'bathrooms': 8,
        'bedrooms': 6,
        'description': 'Siêu phẩm dinh thự đơn lập trực diện vịnh biển và bến du thuyền quốc tế tại Vinhomes Hạ Long '
                       'Xanh. Diện tích đất 500m2 with thiết kế tân cổ điển uy nghi hoàng tráng. Sở hữu 3 mặt sân vườn '
                       'giáp kênh sinh thái lớn và bãi biển riêng nhân tạo. Tiện ích bao gồm rạp chiếu phim gia đình, '
                       'phòng gym, hầm rượu và bể bơi tràn bờ nước mặn.',
        'developer': 'Vinhomes',
        'direction': 'Đông Nam',
        'images': [   'https://s3-hcmc02.higiocloud.vn/intranet/logos/014c719c8e9b4457ad2aba1518049811.png',
                      'https://s3-hcmc02.higiocloud.vn/intranet/logos/43575aabaec24e2180c7355ec771d7cf.png',
                      'https://s3-hcmc02.higiocloud.vn/intranet/logos/2d09497a90d14707ac48cad081fc9395.png'],
        'isPremium': True,
        'legal': 'Sổ đỏ lâu dài',
        'location': 'Phân khu Vịnh Hoàng Gia, Vinhomes Hạ Long Xanh, Quảng Ninh',
        'price': 180.0,
        'pricePerSqm': 360.0,
        'productType': 'villa',
        'productTypeName': 'Biệt thự',
        'projectSlug': 'ha-long-xanh',
        'slug': 'dinh-thu-hoang-gia-mat-bien-ha-long-xanh',
        'status': 'Còn hàng',
        'title': 'Dinh Thự Hoàng Gia Siêu Sang Mặt Biển Hạ Long Xanh - Kỳ Quan Giữa Lòng Kỳ Quan'},
    {   '_id': 'prod-9',
        'area': 300.0,
        'bathrooms': 5,
        'bedrooms': 4,
        'description': 'Biệt thự nghỉ dưỡng 2 tầng sát biển tại Mũi Ông Đội, Phú Quốc. Thiết kế giật cấp độc đáo tôn '
                       'vinh thiên nhiên hoang sơ, sở hữu tầm nhìn 2 mặt biển ngắm hoàng hôn và bình minh tuyệt đẹp. '
                       'Tiêu chuẩn bàn giao full nội thất cao cấp 5 sao quốc tế vận hành bởi tập đoàn danh tiếng.',
        'developer': 'Sun Group',
        'direction': 'Tây Nam',
        'images': [   'https://s3-hcmc02.higiocloud.vn/intranet/logos/46bd1d49542e40e2ae578e7e7d3d1d2a.png',
                      'https://s3-hcmc02.higiocloud.vn/intranet/logos/bd780d5329cf40c2b478879abd121ff9.png',
                      'https://s3-hcmc02.higiocloud.vn/intranet/logos/bdda66b49c314b8898ee6d2daba0f38b.png'],
        'isPremium': True,
        'legal': 'Sổ đỏ lâu dài',
        'location': 'Mũi Ông Đội, An Thới, Phú Quốc',
        'price': 65.0,
        'pricePerSqm': 217.0,
        'productType': 'villa',
        'productTypeName': 'Biệt thự',
        'projectSlug': 'sun-primavera',
        'slug': 'biet-thu-sun-premier-village-phu-quoc',
        'status': 'Còn hàng',
        'title': 'Biệt Thự Sun Premier Village Phú Quốc - Sát Biển Bãi Khem Tuyệt Mỹ'}]

users = [   {   '_id': 'user-1',
        'createdAt': '2026-01-15',
        'email': 'hoainamtin2@gmail.com',
        'hashed_password': 'pbkdf2:sha256:600000$b11d0b6a8d147f82dc3cc31e856ec630$2b1468f659ad99fc69cf3d4da609dea97904a4c820aa17555f6dabc4e6c60b3f',
        'name': 'Administrator',
        'role': 'admin',
        'status': 'active'},
    {   '_id': 'user-2',
        'createdAt': '2026-02-20',
        'email': 'staff@realty.com',
        'hashed_password': 'pbkdf2:sha256:600000$3983546f44fc0cdc1ed95e6eb296ce32$2a4701c93655244b43364fc96078f42b8f460d943ae2736a1e137e57ef3816b5',
        'name': 'Trần Thị Nhân Viên',
        'role': 'staff',
        'status': 'active'},
    {   '_id': 'user-3',
        'createdAt': '2026-03-10',
        'email': 'locked@realty.com',
        'hashed_password': 'pbkdf2:sha256:600000$7bc46c9bca21c5058bef440dd9410361$5eac6de8b837ceabb0cf486f729a39b6bf060f6cf803442ec8fad776906f39b1',
        'name': 'Lê Văn Khóa',
        'role': 'staff',
        'status': 'inactive'}]

posts = [   {   '_id': 'news-1',
        'category': 'Thị trường',
        'content': '<p>Thị trường bất động sản Quảng Ninh liên tục ghi nhận những tín hiệu tích cực trong thời gian '
                   'qua. Động lực chính đến từ việc hoàn thiện đồng bộ hạ tầng giao thông kết nối liên vùng như cao '
                   'tốc Hà Nội - Hải Phòng - Hạ Long - Vân Đồn - Móng Cái, sân bay quốc tế Vân Đồn và cảng tàu khách '
                   'quốc tế Hạ Long.</p><p>Đặc biệt, siêu dự án Vinhomes Hạ Long Xanh quy mô lớn tại trục kinh tế ven '
                   'biển Quảng Yên - Hạ Long khởi công xây dựng đã thổi một luồng sinh khí mới vào toàn khu vực. Giới '
                   'chuyên gia nhận định, phân khúc biệt thự nghỉ dưỡng, shophouse thương mại ven biển sẽ là điểm sáng '
                   'đầu tư trung và dài hạn nhờ khai thác tối đa tiềm năng du lịch 4 mùa của địa phương.</p>',
        'image': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/38a21292d32142aabff228b86d2af76c.png',
        'publishedAt': '2026-05-25',
        'slug': 'bat-dong-san-ven-bien-quang-ninh-but-pha-ha-tang-a8f3b',
        'summary': 'Với việc hoàn thiện các tuyến cao tốc kết nối cùng dự án Hạ Long Xanh được đẩy mạnh triển khai, '
                   'thị trường địa ốc Quảng Ninh đang trở thành thỏi nam châm thu hút dòng vốn đầu tư.',
        'title': 'Bất Động Sản Ven Biển Quảng Ninh Bứt Phá Nhờ Đòn Bẩy Hạ Tầng'},
    {   '_id': 'news-2',
        'category': 'Cẩm nang',
        'content': '<p>Mua chung cư cao cấp là giao dịch có giá trị lớn, đòi hỏi khách hàng phải cực kỳ tỉnh táo trước '
                   'khi đặt bút ký hợp đồng. Dưới đây là những lưu ý quan trọng để đảm bảo an toàn tài '
                   'chính:</p><ul><li>Kiểm tra giấy phép xây dựng, quyết định giao đất và quy hoạch chi tiết 1/500 của '
                   'dự án.</li><li>Kiểm tra văn bản chấp thuận đủ điều kiện bán nhà ở hình thành trong tương lai của '
                   'Sở Xây dựng sở tại.</li><li>Tìm hiểu năng lực tài chính và uy tín của chủ đầu tư thông qua các dự '
                   'án đã bàn giao trước đó (ví dụ như Vinhomes, Masterise Homes với tiến độ ra sổ nhanh '
                   'chóng).</li><li>Đọc kỹ chính sách bảo lãnh ngân hàng cho dự án.</li></ul>',
        'image': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/da383dca5f5647ccb66ebb849124415b.png',
        'publishedAt': '2026-05-18',
        'slug': 'bi-quyet-mua-can-ho-chung-cu-cao-cap-tranh-rui-ro-phap-ly-c4d2e',
        'summary': 'Để không rơi vào cảnh "tiền mất tật mang", người mua nhà cần xem xét kỹ lưỡng hồ sơ pháp lý dự án, '
                   'uy tín chủ đầu tư và các điều khoản trong hợp đồng mua bán.',
        'title': 'Bí Quyết Mua Căn Hộ Chung Cư Cao Cấp Tránh Rủi Ro Pháp Lý'},
    {   '_id': 'news-3',
        'category': 'Quy hoạch',
        'content': '<p>Khu vực phía Đông Hà Nội đang thay đổi diện mạo nhanh chóng từng ngày. Với chiến lược "đa cực" '
                   'trong phát triển không gian thủ đô, trục phía Đông với tâm điểm Gia Lâm và khu vực giáp ranh Văn '
                   'Giang (Hưng Yên) được quy hoạch là cực tăng trưởng kinh tế mới.</p><p>Sự xuất hiện của các đại đô '
                   'thị tỷ đô như Vinhomes Ocean Park 1, 2 và sắp tới là các dự án hạ tầng cầu vượt sông Hồng (cầu '
                   'Trần Hưng Đạo, cầu Giang Biên) sẽ thu hút hàng chục vạn cư dân dịch chuyển từ nội đô cũ ra ngoài, '
                   'biến nơi đây thành khu vực sầm uất bậc nhất phía Bắc.</p>',
        'image': 'https://s3-hcmc02.higiocloud.vn/intranet/logos/acbd7dcd70a34c97a1e999c1bd39d729.png',
        'publishedAt': '2026-05-12',
        'slug': 'ban-do-quy-hoach-do-thi-ve-tinh-phia-dong-ha-noi-f2g4h',
        'summary': 'Quy hoạch xây dựng thủ đô Hà Nội định hướng Gia Lâm và Văn Giang (Hưng Yên) trở thành những trung '
                   'tâm đô thị sinh thái, tri thức hiện đại bậc nhất vùng thủ đô.',
        'title': 'Bản Đồ Quy Hoạch Đô Thị Vệ Tinh Phía Đông Hà Nội Có Gì Mới?'}]

crm_customers = [
    {
        "name": "Nguyễn Văn Hùng",
        "code": "KH-0001",
        "phone": "0987654321",
        "classification": "Tiềm năng",
        "address": "72 Nguyễn Trãi, Thanh Xuân, Hà Nội",
        "email": "hung.nguyen@gmail.com",
        "source": "Facebook",
        "needs": "Tìm mua liền kề Ocean Park 2 khoảng 12 tỷ",
        "note": "Khách thiện chí, đã đi xem thực tế 1 lần",
        "createdAt": "2026-06-01T10:30:00+07:00"
    },
    {
        "name": "Lê Thị Mai",
        "code": "KH-0002",
        "phone": "0912345678",
        "classification": "Đầu tư",
        "address": "Lê Lợi, Quận 1, TP. HCM",
        "email": "mai.le@yahoo.com",
        "source": "Giới thiệu",
        "needs": "Căn hộ Masteri West Heights làm homestay",
        "note": "Nhà đầu tư quen thuộc, tài chính sẵn sàng",
        "createdAt": "2026-06-02T14:45:00+07:00"
    },
    {
        "name": "Phạm Minh Tuấn",
        "code": "KH-0003",
        "phone": "0909998877",
        "classification": "Đầu tư",
        "address": "Vinhomes Riverside, Long Biên, Hà Nội",
        "email": "tuan.pham@vip.com",
        "source": "Website",
        "needs": "Biệt thự đơn lập view biển hồ Ocean Park 1",
        "note": "Khách tài chính cực mạnh, cần tư vấn phân khu Ngọc Trai",
        "createdAt": "2026-06-03T09:15:00+07:00"
    }
]

crm_advisories = [
    {
        "name": "Nguyễn Hoàng Nam",
        "phone": "0977665544",
        "details": "Tôi muốn đăng ký nhận bảng giá dự án Ocean Park 2 phân khu San Hô và chính sách chiết khấu mới nhất.",
        "productSlug": "biet-thu-song-lap-san-ho-gan-cong-vien-song",
        "productName": "Biệt Thự Song Lập San Hô Kế Cận Công Viên Sóng Royal Wave Park",
        "status": "Mới",
        "createdAt": "2026-06-04T11:20:00+07:00"
    },
    {
        "name": "Hoàng Thu Trang",
        "phone": "0933445566",
        "details": "Cần tư vấn căn hộ 2 phòng ngủ view hồ dự án Masteri West Heights, tầng trung, Đông Nam.",
        "productSlug": "can-ho-panorama-masteri-west-heights-toa-a",
        "productName": "Căn Hộ Panorama Masteri West Heights - Tòa A View Trọn Hồ Trung Tâm",
        "status": "Đã liên hệ",
        "createdAt": "2026-06-04T16:00:00+07:00"
    }
]

crm_newsletters = [
    {
        "email": "newsletter1@domain.com",
        "createdAt": "2026-05-20T08:00:00+07:00",
        "active": True
    },
    {
        "email": "newsletter2@domain.com",
        "createdAt": "2026-05-25T09:30:00+07:00",
        "active": True
    },
    {
        "email": "unsubscribed@domain.com",
        "createdAt": "2026-06-01T15:22:00+07:00",
        "active": False
    }
]

def seed_db():
    print(f"Connecting to database '{DB_NAME}'...")
    client = MongoClient(MONGODB_URI)
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

    # Seed CRM Customers
    print("Seeding CRM customers...")
    db["crm_customers"].delete_many({})
    db["crm_customers"].create_index("code", unique=True)
    db["crm_customers"].insert_many(crm_customers)
    print(f"Successfully seeded {len(crm_customers)} CRM customers.")

    # Seed CRM Advisories
    print("Seeding CRM advisories...")
    db["crm_advisories"].delete_many({})
    db["crm_advisories"].insert_many(crm_advisories)
    print(f"Successfully seeded {len(crm_advisories)} CRM advisories.")

    # Seed CRM Newsletters
    print("Seeding CRM newsletters...")
    db["crm_newsletters"].delete_many({})
    db["crm_newsletters"].create_index("email", unique=True)
    db["crm_newsletters"].insert_many(crm_newsletters)
    print(f"Successfully seeded {len(crm_newsletters)} CRM newsletters.")

    # Seed Posts
    print("Seeding posts...")
    db["realty_posts"].delete_many({})
    db["realty_posts"].insert_many(posts)
    print(f"Successfully seeded {len(posts)} posts.")

    print("\nDatabase seeding completed successfully!")
    client.close()

if __name__ == "__main__":
    seed_db()
