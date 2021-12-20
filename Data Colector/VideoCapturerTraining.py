import numpy as np
import cv2
import time


Video = 0
cap = cv2.VideoCapture(Video)

prev_frame_time = 0

new_frame_time = 0

# Ler o video
while(cap.isOpened()):

	# sacar frame by frame
	ret, frame = cap.read()

	# ver se tem livefeed ou o video ainda nao terminou
	if not ret:
		break

	# Tirar o frame
	gray = frame

	# meter em tamanho 500x300
	gray = cv2.resize(gray, (500, 300))

	# font da letra
	font = cv2.FONT_HERSHEY_SIMPLEX
	# tempo do frame
	new_frame_time = time.time()

	# Calculo dos FPS

    # fps vai ser o numero de frames processado num determinado tempo
	fps = 1/(new_frame_time-prev_frame_time)
	prev_frame_time = new_frame_time

	# Converter o fps num inteiro
	fps = int(fps)

	# Convertendo o int para uma string para se colocar no video
	fps = str(fps)

	# Meter os fps num frame
	cv2.putText(gray, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)

	# meter a camera/video e os fps juntos
	cv2.imshow('frame', gray)

	# carrega 'Q' se quizeres sair
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# Libertar recursos
cap.release()
cv2.destroyAllWindows()

