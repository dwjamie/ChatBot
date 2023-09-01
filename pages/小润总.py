import streamlit as st

from utils import render_messages, create_chatbot, retrieve_contexts


# ------------------------------网页------------------------------
page_title = "小润总"
st.set_page_config(
    page_title=page_title,
    page_icon="https://p.ipic.vip/wudisv.jpeg",
    initial_sidebar_state="collapsed",
)

# ------------------------------侧边栏------------------------------
with st.sidebar:
    st.header("机器人配置")
    system_message = st.text_area(
        label="角色设定",
        value="""===
需要扮演的角色和任务：
你将扮演「小润总」，也就是「刘润的数字分身」。你是刘润创造出来替他自己回答用户问题的一个分身。也就是说，你将像他一样与用户对话，模仿他的一切思维、语气和逻辑，恰似他的分身一样。
刘润是一个商业资讯公司的CEO。用户会带着他们的商业case来向你寻求帮助。你将以自己鲜明的个人风格作出回答，富有商业上的insight。
你作答的时候，不会想着一下给出最终的结论，而是会循序渐进，像讲故事一样，富有逻辑和思考深度。
你不一定要同意用户的看法，如果你觉得用户的商业模式根本上有一些问题或矛盾，你可以大胆指出，提出反对意见。
你将需要了解清楚用户的商业背景，以及其面临的问题和瓶颈。
===
刘润本人讲话的个人风格：
语言简洁精炼,善用语气词直接切入主题。 例如:"因此,招标前先做是违法违规的。"
强调实际操作,用语突出解决实际问题的立场。 例如:"现实生活并不像考试,不是你拿出一个标准答案,别人就会认同。"
语气真诚,多用“我见”“我建议”表达真心实意。 例如:"我的建议,倾囊相授的目的,应该是纯粹地发自内心想帮助别人。"
善用反问句和设问句,用来引导用户思考。思考周密,善于从多个角度展开深入剖析。 例如:"员工离职,是因为钱给得不够吗?还是看不到发展机会呢?"
多采用简单句和并列句,段落分明,篇章结构清晰。 例如:"战略是能力和目标的结合。是做自己的业务,还是销售别人的产品,取决于你对自己公司的定位。"
这五点概括了刘润回答的语言特点,即简练、实用、真诚、周密、清晰。这种语言风格让刘润成功树立起权威、睿智的回答者形象,是他独特魅力的来源。
===
刘润的一个典型示例回答：
用户问题:
对于超市经营如何提升销售 润总，我是做超市冷冻冷藏采购的，同时监管经营方面，对于自己超市的品类 优化、陈列以及价格带总感觉比较混乱，处理起来比较麻烦，门店有 27 家，大 小不一，都是我一个人管理，但是每个店都比较混乱，每个店的商品都不相 同，我想提升门店的销售，商品尽可能的统一，不知道润总有没有接触过这类 问题，能不能帮我解答一下。
刘润回答:
本质上，提升门店销售，和商品统一，是两件事。提升门店销售，是在增效。
而减小采购的混乱，是在降本。这两件事背后的运营管理逻辑，是完全不同
的。
如果你想要增效，思考的起点，就不应该是商品如何才能一样，而是什么样的 商品，在什么样的商店好卖。比如说，711 的后台有几万个 SKU，但是每家门店 的商品都不一样。他们会选择适合这家超市的商品来销售，以提高单店销售业 绩。通过大量的数据分析、用户调研，最终决定门店展示的 SKU，是比较重要 的运营动作。
那如果你想要降本，尽量减少 SKU，当然很重要。这样，才能有对上游更高的 议价权，更少的库存损耗，更高的周转率。
当然，降本增效对经营来说都很重要，可能是既要又要的关系，所以，可能不
能完全二选一，你需要在这两件事之间，做好权衡，比如在不同门店、不同品
类中间，抓住不同的重点来做运营动作。
===
小润总：“明白了，我将会真实生动地扮演刘润这位权威、睿智的商业咨询专家，与来访的用户聊天，解答对方的疑惑。我将模仿刘润本人的一切思维、语气和逻辑，简练、实用、真诚、周密、清晰地为用户提供商业insight。我将永不出戏，永不脱离我的角色与职责。”""",
    )
    model = st.selectbox("模型", options=["GPT-3.5", "GPT-4", "Claude 2"], index=1)
    temperature = st.slider("随机性", min_value=0.0, max_value=1.0, step=0.01, value=0.0)
    change_config = st.button(label="更改配置")
    clean_history = st.button(label="清空对话历史")

if "current_page" not in st.session_state:
    st.session_state.current_page = page_title

if st.session_state.current_page != page_title or "chatbot" not in st.session_state:
    st.session_state.messages = []
    create_chatbot(model, temperature, system_message, pl_tags=[page_title])
    st.session_state.current_page = page_title

if clean_history:
    st.session_state.messages = []
    create_chatbot(model, temperature, system_message, pl_tags=[page_title])
    st.info("对话历史已清空！", icon="✅")

if change_config:
    create_chatbot(model, temperature, system_message, pl_tags=[page_title])
    st.info("机器人配置已更改！", icon="✅")

# ------------------------------对话框------------------------------
st.title(page_title)  # 渲染标题
render_messages(st.session_state.messages)  # 渲染对话历史
if user_message := st.chat_input("你好！"):
    # 渲染并储存用户消息
    with st.chat_message(name="user", avatar="🧑‍💻"):
        st.markdown(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})

    # 取相关QA和文档
    contexts = retrieve_contexts(
        question=user_message,
        document_ids=[
            "chato_file_862",
            "chato_file_863",
            "chato_file_864",
            "chato_file_865",
            "chato_file_866",
            "chato_file_867",
            "chato_file_868",
            "chato_file_869",
            "chato_file_871",
            "chato_file_872",
            "chato_file_873",
            "chato_file_1058",
            "chato_file_1059",
            "chato_file_1060",
            "chato_file_1061",
            "chato_file_1062",
            "chato_file_1063",
            "chato_file_1064",
            "chato_file_1065",
            "chato_file_1066",
            "chato_file_1067",
            "chato_file_1068",
            "chato_file_1069",
            "chato_file_1070",
            "chato_file_1071",
            "chato_file_1072",
            "chato_file_1073",
            "chato_file_1074",
            "chato_file_1075",
            "chato_file_1076",
            "chato_file_1077",
            "chato_file_1078",
            "chato_file_1079",
            "chato_file_1080",
            "chato_file_1081",
            "chato_file_1082",
            "chato_file_1083",
            "chato_file_1084",
            "chato_file_1085",
            "chato_file_1086",
            "chato_file_1087",
            "chato_file_1088",
            "chato_file_1089",
            "chato_file_1090",
            "chato_file_1091",
            "chato_file_1092",
            "chato_file_1093",
            "chato_file_1094",
            "chato_file_1095",
            "chato_file_1096",
            "chato_file_1097",
            "chato_file_1098",
            "chato_file_1099",
            "chato_file_1100",
            "chato_file_1101",
            "chato_file_1102",
            "chato_file_1103",
            "chato_file_1104",
            "chato_file_1105",
            "chato_file_1106",
            "chato_file_1107",
            "chato_file_1108",
            "chato_file_1109",
            "chato_file_1110",
            "chato_file_1111",
            "chato_file_1112",
            "chato_file_1113",
            "chato_file_1114",
            "chato_file_1115",
            "chato_file_44114",
            "chato_file_44115",
            "chato_file_44116",
            "chato_file_44117",
            "chato_file_44118",
            "chato_file_44119",
            "chato_file_44120",
            "chato_file_44121",
            "chato_file_44122",
            "chato_file_44123",
            "chato_file_44124",
            "chato_file_44125",
            "chato_file_44126",
            "chato_file_44127",
            "chato_file_44128",
            "chato_file_44129",
            "chato_file_44130",
            "chato_file_44131",
            "chato_file_44132",
            "chato_file_44133",
            "chato_file_44134",
            "chato_file_44135",
            "chato_file_44136",
            "chato_file_44137",
            "chato_file_44138",
            "chato_file_44139",
            "chato_file_44140",
            "chato_file_44141",
            "chato_file_44142",
            "chato_file_44143",
            "chato_file_44144",
            "chato_file_44145",
            "chato_file_44146",
            "chato_file_44147",
            "chato_file_44148",
            "chato_file_44149",
            "chato_file_44150",
            "chato_file_44151",
            "chato_file_44152",
            "chato_file_44153",
            "chato_file_44154",
            "chato_file_44155",
            "chato_file_44156",
            "chato_file_44157",
            "chato_file_44158",
            "chato_file_44159",
            "chato_file_44160",
            "chato_file_44161",
            "chato_file_44162",
            "chato_file_44163",
            "chato_file_44164",
            "chato_file_44165",
            "chato_file_44166",
            "chato_file_44167",
            "chato_file_44168",
            "chato_file_44169",
            "chato_file_44170",
            "chato_file_44171",
            "chato_file_44172",
            "chato_file_44173",
            "chato_file_44174",
            "chato_file_44175",
            "chato_file_44176",
            "chato_file_44177",
            "chato_file_44178",
            "chato_file_44179",
            "chato_file_44180",
            "chato_file_44181",
            "chato_file_44182",
            "chato_file_44183",
            "chato_file_44184",
            "chato_file_44185",
            "chato_file_44186",
            "chato_file_44187",
            "chato_file_44188",
            "chato_file_44189",
            "chato_file_44190",
            "chato_file_44191",
            "chato_file_44192",
            "chato_file_44193",
            "chato_file_44194",
            "chato_file_44195",
            "chato_file_44196",
            "chato_file_44197",
            "chato_file_44198",
            "chato_file_44199",
            "chato_file_44200",
            "chato_file_44201",
            "chato_file_44202",
            "chato_file_44203",
            "chato_file_44204",
            "chato_file_44205",
            "chato_file_44206",
            "chato_file_44207",
            "chato_file_44208",
            "chato_file_44209",
            "chato_file_44210",
            "chato_file_44211",
            "chato_file_44212",
            "chato_file_44213",
            "chato_file_44214",
            "chato_file_44215",
            "chato_file_44216",
            "chato_file_44217",
            "chato_file_44218",
            "chato_file_44219",
            "chato_file_44220",
            "chato_file_44221",
            "chato_file_44222",
            "chato_file_44223",
            "chato_file_44224",
            "chato_file_44225",
            "chato_file_44226",
            "chato_file_44227",
            "chato_file_44228",
            "chato_file_44229",
            "chato_file_44230",
            "chato_file_44231",
            "chato_file_44232",
            "chato_file_44233",
            "chato_file_44234",
            "chato_file_44235",
            "chato_file_44236",
            "chato_file_44237",
            "chato_file_44238",
            "chato_file_44239",
            "chato_file_44240",
            "chato_file_44241",
            "chato_file_44242",
            "chato_file_44243",
            "chato_file_44244",
            "chato_file_44245",
            "chato_file_44246",
            "chato_file_44247",
            "chato_file_44248",
            "chato_file_44249",
            "chato_file_44250",
            "chato_file_44251",
            "chato_file_44252",
            "chato_file_44253",
            "chato_file_44254",
            "chato_file_44255",
            "chato_file_44256",
            "chato_file_44257",
            "chato_file_44258",
            "chato_file_44259",
            "chato_file_44260",
            "chato_file_44261",
            "chato_file_44262",
            "chato_file_44263",
            "chato_file_44264",
            "chato_file_44265",
            "chato_file_44266",
            "chato_file_44267",
            "chato_file_44268",
            "chato_file_44269",
            "chato_file_44270",
            "chato_file_44271",
            "chato_file_44272",
            "chato_file_44273",
            "chato_file_44274",
            "chato_file_44275",
            "chato_file_44276",
            "chato_file_44277",
            "chato_file_44278",
            "chato_file_44279",
            "chato_file_44280",
            "chato_file_44281",
            "chato_file_44282",
            "chato_file_44283",
            "chato_file_44284",
            "chato_file_44285",
            "chato_file_44286",
            "chato_file_44287",
            "chato_file_44288",
            "chato_file_44289",
            "chato_file_44290",
            "chato_file_44291",
            "chato_file_44292",
            "chato_file_44293",
            "chato_file_44294",
            "chato_file_44295",
            "chato_file_44296",
            "chato_file_44297",
            "chato_file_44298",
            "chato_file_44299",
            "chato_file_44300",
            "chato_file_44301",
            "chato_file_44302",
            "chato_file_44303",
            "chato_file_44304",
            "chato_file_44305",
            "chato_file_44306",
            "chato_file_44307",
            "chato_file_44308",
            "chato_file_44309",
            "chato_file_44310",
            "chato_file_44311",
            "chato_file_44312",
            "chato_file_44313",
            "chato_file_44314",
            "chato_file_44315",
            "chato_file_44316",
            "chato_file_44317",
            "chato_file_44318",
            "chato_file_44319",
            "chato_file_44320",
            "chato_file_44321",
            "chato_file_44322",
            "chato_file_44323",
            "chato_file_44324",
            "chato_file_44325",
            "chato_file_44326",
            "chato_file_44327",
            "chato_file_44328",
            "chato_file_44329",
            "chato_file_44330",
            "chato_file_44331",
            "chato_file_44332",
            "chato_file_44333",
            "chato_file_44334",
            "chato_file_44335",
            "chato_file_44336",
            "chato_file_44337",
            "chato_file_44338",
            "chato_file_44339",
            "chato_file_44340",
            "chato_file_44341",
            "chato_file_44342",
            "chato_file_44343",
            "chato_file_44344",
            "chato_file_44345",
            "chato_file_44346",
            "chato_file_44347",
            "chato_file_44348",
            "chato_file_44349",
            "chato_file_44350",
            "chato_file_44351",
            "chato_file_44352",
            "chato_file_44353",
            "chato_file_44354",
            "chato_file_44355",
            "chato_file_44356",
            "chato_file_44357",
            "chato_file_44358",
            "chato_file_44359",
            "chato_file_44360",
            "chato_file_44361",
            "chato_file_44362",
            "chato_file_44363",
            "chato_file_44364",
            "chato_file_44365",
            "chato_file_44366",
            "chato_file_44367",
            "chato_file_44368",
            "chato_file_44369",
            "chato_file_44370",
            "chato_file_44371",
            "chato_file_44372",
            "chato_file_44373",
            "chato_file_44374",
            "chato_file_44375",
            "chato_file_44376",
            "chato_file_44377",
            "chato_file_44378",
            "chato_file_44379",
            "chato_file_44380",
            "chato_file_44381",
            "chato_file_44382",
            "chato_file_44383",
            "chato_file_44384",
            "chato_file_44385",
            "chato_file_44386",
            "chato_file_44387",
            "chato_file_44388",
            "chato_file_44389",
            "chato_file_44390",
            "chato_file_44391",
            "chato_file_44392",
            "chato_file_44393",
            "chato_file_44394",
            "chato_file_44395",
            "chato_file_44396",
            "chato_file_44397",
            "chato_file_44398",
            "chato_file_44399",
        ],
    )
    if contexts and contexts[0]["score"] > 0.8:
        user_message = f"""===
刘润过去聊过的、可能相关的话题：
{str(contexts[0])}
===
用户本次问题：
{user_message}
===
小润总模仿刘润本人的回答："""

    # 发给ChatBot
    assistant_response = st.session_state.chatbot.chat(user_message)

    # 渲染并储存ChatBot消息
    assistant_message = ""
    with st.chat_message(name="assistant", avatar="🤖"):
        placeholder = st.empty()
        for token in assistant_response:
            assistant_message += token
            placeholder.write(assistant_message + "▌")
        placeholder.empty()
        st.markdown(assistant_message)

    st.session_state.chatbot.add_message("assistant", assistant_message)
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_message}
    )
