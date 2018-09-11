from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_details(url):
    html = urlopen(url)
    res = BeautifulSoup(html.read());
    tags = res.find_all("td")

    response = {}
    for i in range(len(tags)):
        if(tags[i].getText() == 'Nome:'):
            response['nome'] = tags[i+1].getText()

        if(tags[i].getText() == 'Cargo:'):
            response['cargo'] = tags[i+1].getText()

        if(tags[i].getText() == 'Função:'):
            response['funcao'] = tags[i+1].getText()

        if(tags[i].getText() == 'Lotação:'):
            response['lotacao'] = tags[i+1].getText()

        if(tags[i].getText() == 'Escolaridade / Titulação:'):
            response['escolaridade'] = tags[i+1].getText()

        if(tags[i].getText() == 'Tempo de Serviço:'):
            response['tempo_de_servico'] = int(tags[i+1].getText().replace(" anos", ""))

        if(tags[i].getText() == 'Total Bruto:'):
            response['total_bruto'] = float(tags[i+1].getText().replace("R$ ", "").replace(".", "").replace(",", "."))
            response['total_bruto_string'] = tags[i+1].getText()

        if(tags[i].getText() == 'Total Líquido: '):
            try:
                response['total_liquido'] = float(tags[i+1].getText().replace("R$ ", "").split('\t')[0].replace(".", "").replace(",", "."))
                response['total_liquido_string'] = tags[i+1].getText()
            except ValueError:
                response['total_liquido'] = 'none'
                response['total_liquido_string'] = 'none'
        
        m_r = res.find_all("h3")[0]
        response['mes_referencia'] = m_r.getText()

    return response;

# {
#         "nome"   : tags[1].getText(),
#         "cargo"  : tags[3].getText(),
#         "funcao" :tags[5].getText(),
#         "lotacao":tags[7].getText(),
#         "escolaridade"    :tags[9].getText(),
#         "tempo_de_servico":tags[11].getText(),
#         "total_bruto"       : tags[23].getText().replace("R$ ", ""),
#         "total_bruto_string": tags[23].getText(),
#         "total_liquido"     :tags[-1].getText().replace("R$ ", "").split('\t')[0],
#         "total_liquido_string" : tags[-1].getText()
#     }

html = urlopen("http://transparencia.uepb.edu.br/consulta/")
res = BeautifulSoup(html.read());

tags = res.find_all("tr")

print("total_liquido_string,total_liquido,total_bruto,cargo,lotacao,funcao,total_bruto_string,tempo_de_servico,escolaridade,nome")
for t in tags:
    url = t.contents[1].contents[1].get("href")
    details = get_details(url)
    print("{} {} {} {} {} {} {} {} {} {} {}"
        .format(
            details['nome'],
            details['cargo'],
            details['funcao'],
            details['lotacao'],
            details['escolaridade'],
            details['tempo_de_servico'],
            details['total_bruto'],
            details['total_bruto_string'],
            details['total_liquido'],
            details['total_liquido_string'],
            details['mes_referencia']
        )
    )
    # print({
    #     "funcao": t.contents[3].getText(),
    #     "cargo" : t.contents[5].getText(),
    #     "url"   : t.contents[1].contents[1].get("href")
    # })
    # print(t.contents[3].getText())#funcao
    # print(t.contents[5].getText()) #cargo
    # print(t.contents[1].contents[1].get("href"))#url
