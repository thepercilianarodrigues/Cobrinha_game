import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CINZA,
    CAMINHO_RECORDE,
    CAMINHO_SPRITES,
)

from src.funcoes import (
    calcular_pontos,
    jogador_perdeu,
    limitar_valor,
    verificar_colisao,
    tomar_dano,
    celula_para_pixel,
    posicao_aleatoria,
    sortear_tipo_alimento,
    desenhar_grade,
    desenhar_cobra,
    cor_alimento,
    desenhar_alimento,
    desenhar_hud,
    desenhar_tela_inicial,
    desenhar_game_over,
    inicializar_estado,
    processar_eventos,
    atualizar_estado,
)
from src.sprites import pegar_sprite
from src.dados import (
    salvar_recorde,
    carregar_recorde,
)


def executar_jogo():
    """Executa o loop principal do jogo e controla estado, colisões e pontuação."""
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Snake Game — Fundamentos de AEDS")

    fonte = pygame.font.SysFont("monospace", 18, bold=True)
    fonte_grande = pygame.font.SysFont("monospace", 52, bold=True)

    relogio = pygame.time.Clock()

    # ── Tela inicial ──
    desenhar_tela_inicial(tela, fonte_grande, fonte)
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                esperando = False

    while True:
        estado = inicializar_estado()

        # ── Loop de jogo ──
        while estado["rodando"]:
            estado = processar_eventos(estado)
            estado = atualizar_estado(estado)

            # ── Renderização ──
            tela.fill(PRETO)
            desenhar_grade(tela)
            desenhar_cobra(tela, estado["corpo"])
            desenhar_alimento(tela, estado["pos_alimento"], estado["tipo_alimento"])
            desenhar_hud(tela, fonte,
                         estado["pontos"],
                         estado["vidas"],
                         estado["imune"],
                         estado["ticks_fim_imunidade"],
                         estado["velocidade"])

            pygame.display.flip()
            relogio.tick(estado["velocidade"])

        # ── Game Over ──
        desenhar_game_over(tela, fonte_grande, fonte, estado["pontos"])
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        esperando = False
                    elif evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

