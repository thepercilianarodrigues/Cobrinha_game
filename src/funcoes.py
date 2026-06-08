def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos ganhos à pontuação atual."""
    return pontos_atual + pontos_ganhos


def tomar_dano(vida_atual, dano):
    """Reduz a vida atual com base no dano recebido."""
    return vida_atual - dano


def jogador_perdeu(vidas):
    """Indica se o jogador ficou sem vidas."""
    return vidas <= 0


def limitar_valor(valor, minimo, maximo):
    """Mantém um valor dentro do intervalo [minimo, maximo]."""
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def verificar_colisao(retangulo_1, retangulo_2):
    """Verifica sobreposição entre dois retângulos do Pygame."""
    return retangulo_1.colliderect(retangulo_2)

def celula_para_pixel(col, lin):
    """Converte coordenada de grade para pixel (centro da célula)."""
    return col * TAMANHO_CELULA, lin * TAMANHO_CELULA


def posicao_aleatoria(excluir=None):
    """Retorna uma posição aleatória na grade, evitando posições em 'excluir'."""
    excluir = excluir or []
    while True:
        pos = (random.randint(0, COLUNAS - 1), random.randint(0, LINHAS - 1))
        if pos not in excluir:
            return pos


def sortear_tipo_alimento():
    """Sorteia o tipo de alimento com probabilidades diferentes."""
    r = random.random()
    if r < 0.65:
        return COMUM
    elif r < 0.90:
        return BONUS
    else:
        return RARO


def desenhar_grade(tela):
    """Desenha linhas de grade sutis no fundo."""
    for x in range(0, LARGURA, TAMANHO_CELULA):
        pygame.draw.line(tela, (30, 30, 30), (x, 0), (x, ALTURA))
    for y in range(0, ALTURA, TAMANHO_CELULA):
        pygame.draw.line(tela, (30, 30, 30), (0, y), (LARGURA, y))


def desenhar_cobra(tela, corpo):
    """Desenha cada segmento da cobra."""
    for i, (col, lin) in enumerate(corpo):
        x, y = celula_para_pixel(col, lin)
        cor = VERDE if i > 0 else VERDE_ESC  # cabeça mais escura
        pygame.draw.rect(tela, cor, (x + 1, y + 1, TAMANHO_CELULA - 2, TAMANHO_CELULA - 2), border_radius=4)


def cor_alimento(tipo):
    if tipo == COMUM:
        return VERMELHO
    elif tipo == BONUS:
        return AMARELO
    else:
        return ROXO


def desenhar_alimento(tela, pos, tipo):
    """Desenha o alimento na tela."""
    col, lin = pos
    x, y = celula_para_pixel(col, lin)
    cx = x + TAMANHO_CELULA // 2
    cy = y + TAMANHO_CELULA // 2
    raio = TAMANHO_CELULA // 2 - 2
    pygame.draw.circle(tela, cor_alimento(tipo), (cx, cy), raio)
    # brilho
    pygame.draw.circle(tela, BRANCO, (cx - 3, cy - 3), 3)


def desenhar_hud(tela, fonte, pontos, vidas, imune, ticks_imune, fps_atual):
    """Desenha pontuação, vidas e status de imunidade."""
    # Fundo do HUD (faixa superior)
    pygame.draw.rect(tela, (20, 20, 20), (0, 0, LARGURA, 30))
    pygame.draw.line(tela, VERDE_ESC, (0, 30), (LARGURA, 30), 1)

    txt_pts = fonte.render(f"Pontos: {pontos}", True, BRANCO)
    txt_vidas = fonte.render(f"Vidas: {'♥ ' * vidas}", True, VERMELHO)

    tela.blit(txt_pts, (10, 6))
    tela.blit(txt_vidas, (LARGURA // 2 - 60, 6))

    if imune:
        seg_restante = round((ticks_imune - pygame.time.get_ticks()) / 1000, 1)
        txt_imune = fonte.render(f"IMUNE: {seg_restante}s", True, ROXO)
        tela.blit(txt_imune, (LARGURA - 150, 6))


def desenhar_tela_inicial(tela, fonte_grande, fonte):
    tela.fill(PRETO)
    titulo = fonte_grande.render("🐍  SNAKE GAME", True, VERDE)
    instrucoes = [
        "Use as setas do teclado para mover a cobra.",
        "",
        "🔴 Alimento Comum  →  +5 pontos  (frequente)",
        "🟡 Alimento Bônus  →  +10 pontos  (ocasional)",
        "🟣 Alimento Raro   →  Imunidade por 5 s  (raro)",
        "",
        "Você começa com 3 vidas.",
        "Colidir com a parede ou com o próprio corpo perde 1 vida.",
        "",
        "Pressione ENTER para começar!",
    ]
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 80))
    for i, linha in enumerate(instrucoes):
        cor = AMARELO if "10 pontos" in linha else (ROXO if "Imunidade" in linha else BRANCO)
        surf = fonte.render(linha, True, cor)
        tela.blit(surf, (LARGURA // 2 - surf.get_width() // 2, 200 + i * 32))
    pygame.display.flip()


def desenhar_game_over(tela, fonte_grande, fonte, pontos):
    tela.fill(PRETO)
    txt = fonte_grande.render("GAME OVER", True, VERMELHO)
    pts = fonte.render(f"Pontuação final: {pontos}", True, BRANCO)
    reiniciar = fonte.render("Pressione ENTER para jogar novamente  |  ESC para sair", True, CINZA)
    tela.blit(txt, (LARGURA // 2 - txt.get_width() // 2, 200))
    tela.blit(pts, (LARGURA // 2 - pts.get_width() // 2, 300))
    tela.blit(reiniciar, (LARGURA // 2 - reiniciar.get_width() // 2, 380))
    pygame.display.flip()

def inicializar_estado():
    """Retorna o estado inicial do jogo."""
    corpo = [(COLUNAS // 2, LINHAS // 2),
             (COLUNAS // 2 - 1, LINHAS // 2),
             (COLUNAS // 2 - 2, LINHAS // 2)]
    direcao = (1, 0)  # movendo para a direita
    pos_alimento = posicao_aleatoria(excluir=corpo)
    tipo_alimento = sortear_tipo_alimento()
    return {
        "corpo": corpo,
        "direcao": direcao,
        "pos_alimento": pos_alimento,
        "tipo_alimento": tipo_alimento,
        "pontos": 0,
        "vidas": 3,
        "imune": False,
        "ticks_fim_imunidade": 0,
        "velocidade": FPS,
        "rodando": True,
    }


def processar_eventos(estado):
    """Lida com entradas do teclado."""
    dx, dy = estado["direcao"]
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP    and dy == 0:
                estado["direcao"] = (0, -1)
            elif evento.key == pygame.K_DOWN  and dy == 0:
                estado["direcao"] = (0, 1)
            elif evento.key == pygame.K_LEFT  and dx == 0:
                estado["direcao"] = (-1, 0)
            elif evento.key == pygame.K_RIGHT and dx == 0:
                estado["direcao"] = (1, 0)
    return estado


def atualizar_estado(estado):
    """Move a cobra e verifica colisões/coletas."""
    corpo = estado["corpo"]
    dx, dy = estado["direcao"]
    cabeca = (corpo[0][0] + dx, corpo[0][1] + dy)

    # Verificar imunidade expirada
    if estado["imune"] and pygame.time.get_ticks() >= estado["ticks_fim_imunidade"]:
        estado["imune"] = False

    # ── Colisão com parede ──
    col, lin = cabeca
    if col < 0 or col >= COLUNAS or lin < 0 or lin >= LINHAS:
        if not estado["imune"]:
            estado["vidas"] -= 1
            if estado["vidas"] <= 0:
                estado["rodando"] = False
                return estado
            # Reposicionar no centro
            estado["corpo"] = [(COLUNAS // 2, LINHAS // 2),
                                (COLUNAS // 2 - 1, LINHAS // 2),
                                (COLUNAS // 2 - 2, LINHAS // 2)]
            estado["direcao"] = (1, 0)
        else:
            # Imune: atravessa a parede (teletransporte)
            cabeca = (col % COLUNAS, lin % LINHAS)
            corpo = [cabeca] + corpo[:-1]
            estado["corpo"] = corpo
        return estado

    # ── Colisão com o próprio corpo ──
    if cabeca in corpo[1:]:
        if not estado["imune"]:
            estado["vidas"] -= 1
            if estado["vidas"] <= 0:
                estado["rodando"] = False
                return estado
            estado["corpo"] = [(COLUNAS // 2, LINHAS // 2),
                                (COLUNAS // 2 - 1, LINHAS // 2),
                                (COLUNAS // 2 - 2, LINHAS // 2)]
            estado["direcao"] = (1, 0)
        return estado

    # ── Mover cobra ──
    novo_corpo = [cabeca] + corpo[:-1]

    # ── Comer alimento ──
    if cabeca == estado["pos_alimento"]:
        tipo = estado["tipo_alimento"]
        if tipo == COMUM:
            estado["pontos"] += 5
        elif tipo == BONUS:
            estado["pontos"] += 10
        elif tipo == RARO:
            estado["imune"] = True
            estado["ticks_fim_imunidade"] = pygame.time.get_ticks() + 5000

        # Crescer: mantém a cauda ao invés de remover
        novo_corpo = [cabeca] + corpo

        # Aumentar velocidade a cada 50 pontos
        estado["velocidade"] = FPS + (estado["pontos"] // 50)

        # Novo alimento
        estado["pos_alimento"] = posicao_aleatoria(excluir=novo_corpo)
        estado["tipo_alimento"] = sortear_tipo_alimento()

    estado["corpo"] = novo_corpo
    return estado
